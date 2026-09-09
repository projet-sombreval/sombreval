"use strict";

/* Le navigateur ne connaît aucune règle du jeu.
 *
 * Il fait trois choses : demander son écran au serveur une fois par seconde,
 * l'afficher, et renvoyer ce que le joueur a cliqué. Tout ce qui raconte
 * l'histoire (noms des rôles, textes, couleurs) vient du serveur, qui le lit
 * dans regles/. Ne restent ici que les mots de l'interface — « Entrer »,
 * « Copier » —, les mêmes dans les trois univers.
 */

const RYTHME = 1000;              // millisecondes entre deux demandes
const EVENEMENTS_AFFICHES = 5;    // longueur du journal à l'écran

const etat = {
  partie: null,
  jeton: null,
  pseudo: "",
  univers: [],
  boucle: null,
};

/* ------------------------------------------------------------------ outils */

function dessiner(html) {
  document.getElementById("ecran").innerHTML = html;
}

function echapper(texte) {
  // Un pseudonyme est écrit par un joueur : on ne le pose jamais tel quel
  // dans la page, sinon on pourrait y glisser du code.
  const boite = document.createElement("div");
  boite.textContent = texte;
  return boite.innerHTML;
}

function remplir(modele, numero) {
  return modele.replace("{numero}", numero);
}

function signaler(texte) {
  const message = document.getElementById("message");
  message.textContent = texte;
  message.hidden = !texte;
}

async function demander(url, options) {
  const reponse = await fetch(url, options);
  const donnees = await reponse.json();
  if (!reponse.ok) {
    throw new Error(donnees.erreur || "Le serveur a refusé.");
  }
  signaler("");
  return donnees;
}

function lire(url) {
  return demander(url);
}

function poster(url, corps) {
  return demander(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(corps),
  });
}

function appliquerLesCouleurs(couleurs) {
  // Les couleurs de l'univers deviennent les variables de la feuille de style.
  for (const nom in couleurs || {}) {
    document.documentElement.style.setProperty("--" + nom, couleurs[nom]);
  }
}

/* ------------------------------------------------------- avant la partie */

async function demarrer() {
  try {
    etat.univers = await lire("/api/univers");
  } catch (souci) {
    signaler(souci.message);
    return;
  }
  appliquerLesCouleurs(premierUnivers().couleurs);

  etat.partie = new URLSearchParams(window.location.search).get("partie");
  etat.jeton = etat.partie && sessionStorage.getItem("jeton:" + etat.partie);

  if (etat.partie && etat.jeton) {
    lancerLaBoucle();
  } else {
    ecranConnexion();
  }
}

function premierUnivers() {
  return etat.univers.find((univers) => univers.disponible) || {};
}

function ecranConnexion() {
  const univers = premierUnivers();
  dessiner(`
    <h1>${echapper(univers.titre || "")}</h1>
    <p class="sous-titre">${univers.annee} — ${echapper(univers.sous_titre || "")}</p>
    <p class="consigne">${etat.partie
      ? "On t'a invité à une partie. Choisis ton nom."
      : "Ouvre une partie, puis envoie le lien à ceux que tu veux voir jouer."}</p>
    <label for="pseudo">Ton pseudonyme</label>
    <input id="pseudo" maxlength="20" autocomplete="off">
    <button class="large" onclick="entrer()">Entrer</button>
  `);
  document.getElementById("pseudo").focus();
}

async function entrer() {
  const pseudo = document.getElementById("pseudo").value.trim();
  if (!pseudo) {
    signaler("Il faut un pseudonyme.");
    return;
  }
  etat.pseudo = pseudo;

  if (etat.partie) {
    await rejoindreLaPartie();
  } else {
    ecranChoixDeLUnivers();
  }
}

function ecranChoixDeLUnivers() {
  const choix = etat.univers.map((univers) => `
    <li><button onclick="creerLaPartie('${univers.nom}')" ${univers.disponible ? "" : "disabled"}>
      ${echapper(univers.titre)} ${univers.annee}<br>
      <small>${univers.disponible ? echapper(univers.sous_titre) : "bientôt"}</small>
    </button></li>`).join("");

  dessiner(`
    <h1>Trois villages</h1>
    <p class="sous-titre">Celui que tu choisis vaut pour tout le monde.</p>
    <ul class="choix">${choix}</ul>
  `);
}

async function creerLaPartie(nom) {
  try {
    memoriser(await poster("/api/parties", { pseudo: etat.pseudo, univers: nom }));
    lancerLaBoucle();
  } catch (souci) {
    signaler(souci.message);
  }
}

async function rejoindreLaPartie() {
  try {
    memoriser(await poster(`/api/parties/${etat.partie}/joueurs`, { pseudo: etat.pseudo }));
    lancerLaBoucle();
  } catch (souci) {
    signaler(souci.message);
  }
}

function memoriser(reponse) {
  etat.partie = reponse.partie;
  etat.jeton = reponse.jeton;
  // Le jeton reste dans cet onglet : c'est lui qui prouve qui je suis.
  sessionStorage.setItem("jeton:" + etat.partie, etat.jeton);
  history.replaceState(null, "", "/?partie=" + etat.partie);
}

/* ------------------------------------------------------ pendant la partie */

function lancerLaBoucle() {
  rafraichir();
  etat.boucle = setInterval(rafraichir, RYTHME);
}

async function rafraichir() {
  try {
    afficher(await lire(`/api/parties/${etat.partie}/vue?jeton=${etat.jeton}`));
  } catch (souci) {
    // Le serveur ne nous connaît plus (il a redémarré, ou la partie est
    // finie) : on arrête de demander et on repart de l'écran d'entrée.
    clearInterval(etat.boucle);
    sessionStorage.clear();
    etat.partie = null;
    etat.jeton = null;
    ecranConnexion();
    signaler(souci.message);
  }
}

function afficher(vue) {
  appliquerLesCouleurs(vue.univers.couleurs);
  if (vue.phase === "attente") return ecranSalleDAttente(vue);
  if (vue.phase === "decouverte") return ecranDecouverteDuRole(vue);
  if (vue.phase === "nuit") return ecranVillageQuiDort(vue);
  if (vue.phase === "jour") return ecranVillageEveille(vue);
  if (vue.phase === "fin") return ecranFinal(vue);
}

async function agir(action, valeur) {
  try {
    afficher(await poster(`/api/parties/${etat.partie}/actions`,
      { jeton: etat.jeton, action: action, valeur: valeur }));
  } catch (souci) {
    signaler(souci.message);
  }
}

function choisir(numero) { agir("choisir", numero); }
function voter(numero) { agir("voter", numero); }
function dire(numero) { agir("dire", numero); }

async function commencerLaPartie() {
  try {
    afficher(await poster(`/api/parties/${etat.partie}/commencer`, { jeton: etat.jeton }));
  } catch (souci) {
    signaler(souci.message);
  }
}

/* ------------------------------------------------------------- les écrans */

function ecranSalleDAttente(vue) {
  const textes = vue.univers.textes;
  const lien = window.location.origin + "/?partie=" + vue.partie;
  const complet = vue.joueurs.length === vue.joueurs_attendus;

  dessiner(`
    <h1>${echapper(vue.univers.titre)}</h1>
    <p class="sous-titre">${vue.univers.annee} — ${echapper(vue.univers.sous_titre)}</p>
    <p class="consigne">${echapper(vue.univers.presentation)}</p>

    <h2>${echapper(textes.attente_titre)}</h2>
    <p>${echapper(textes.attente_consigne)}</p>
    <div class="lien">
      <input id="lien" value="${echapper(lien)}" readonly>
      <button onclick="copierLeLien()">Copier</button>
    </div>

    <h2>Le village (${vue.joueurs.length} sur ${vue.joueurs_attendus})</h2>
    <ul class="village">
      ${vue.joueurs.map((joueur) => `<li>${echapper(joueur.pseudo)}</li>`).join("")}
    </ul>

    ${vue.je_suis_le_createur ? `
      <button class="large" onclick="commencerLaPartie()" ${complet ? "" : "disabled"}>
        ${complet ? "Commencer la partie" : "On attend le village…"}
      </button>` : `<p class="patiente">La partie commencera bientôt.</p>`}
  `);
}

function copierLeLien() {
  const champ = document.getElementById("lien");
  champ.select();
  if (!navigator.clipboard) {
    signaler("Le lien est sélectionné : copie-le à la main.");
    return;
  }
  navigator.clipboard.writeText(champ.value).then(
    () => signaler("Lien copié."),
    () => signaler("Le navigateur a refusé : le lien est sélectionné, copie-le.")
  );
}

function ecranDecouverteDuRole(vue) {
  const textes = vue.univers.textes;
  dessiner(`
    <h2>${echapper(textes.decouverte_titre)}</h2>
    <div class="role">
      <p class="role-nom">${echapper(vue.moi.role.nom)}</p>
      <p class="role-camp">${echapper(vue.moi.role.camp)}</p>
      <p class="role-pouvoir">${echapper(vue.moi.role.pouvoir)}</p>
    </div>
    <p class="consigne">${echapper(textes.decouverte_consigne)}</p>
    ${minuterie(vue)}
  `);
}

function ecranVillageQuiDort(vue) {
  const textes = vue.univers.textes;
  const cibles = vue.cibles || [];

  dessiner(`
    <h1>${echapper(textes.nuit_titre)}</h1>
    <p class="sous-titre">${remplir(textes.nuit_numero, vue.numero_de_nuit)}</p>
    ${consigne(vue)}

    ${cibles.length ? `<ul class="choix">${boutonsDeCible(vue, cibles)}</ul>` : ""}
    ${vue.mon_choix ? `<p class="patiente">${echapper(textes.nuit_choix_fait)}</p>` : ""}
    ${choixDesAllies(vue)}
    ${mesSecrets(vue)}
    ${minuterie(vue)}
  `);
}

function boutonsDeCible(vue, cibles) {
  return cibles.map((numero) => {
    const joueur = vue.joueurs.find((j) => j.numero === numero);
    const choisi = vue.mon_choix === numero ? "choisi" : "";
    return `<li><button class="${choisi}" onclick="choisir('${numero}')">
      ${echapper(joueur.pseudo)}</button></li>`;
  }).join("");
}

function choixDesAllies(vue) {
  const allies = vue.choix_des_allies || [];
  if (allies.length < 2) return "";
  const lignes = allies.map((allie) => `<p>${echapper(allie.pseudo)} :
    ${allie.cible ? echapper(allie.cible) : "n'a pas encore choisi"}</p>`).join("");
  return `<div class="secret">${lignes}</div>`;
}

function ecranVillageEveille(vue) {
  const textes = vue.univers.textes;
  dessiner(`
    <h1>${echapper(textes.jour_titre)}</h1>
    <p class="sous-titre">${remplir(textes.jour_numero, vue.numero_de_nuit)}</p>

    <h2>Ce qui s'est passé</h2>
    ${journal(vue)}

    ${consigne(vue)}
    <h2>Le village</h2>
    <ul class="choix">${boutonsDeVote(vue)}</ul>
    ${listeDesMorts(vue)}

    ${vue.messages.length ? `<h2>Dire quelque chose</h2>
      <ul class="choix">${boutonsDeMessage(vue)}</ul>` : ""}
    ${discussion(vue)}
    ${mesSecrets(vue)}
    ${minuterie(vue)}
  `);
}

function boutonsDeVote(vue) {
  return vue.joueurs
    .filter((joueur) => joueur.vivant && joueur.numero !== vue.moi.numero)
    .map((joueur) => {
      const voix = vue.voix[joueur.numero] || 0;
      const choisi = vue.mon_vote === joueur.numero ? "choisi" : "";
      return `<li><button class="${choisi}" onclick="voter('${joueur.numero}')"
        ${vue.moi.vivant ? "" : "disabled"}>
        ${echapper(joueur.pseudo)}<span class="voix">${voix}</span></button></li>`;
    }).join("");
}

function listeDesMorts(vue) {
  const morts = vue.joueurs.filter((joueur) => !joueur.vivant);
  if (!morts.length) return "";
  return `<ul class="village">${morts.map((joueur) => `
    <li class="mort">${echapper(joueur.pseudo)}
      <span class="role-revele">— ${echapper(joueur.role)}</span></li>`).join("")}</ul>`;
}

function boutonsDeMessage(vue) {
  return vue.messages.map((texte, numero) =>
    `<li><button onclick="dire(${numero})">${echapper(texte)}</button></li>`).join("");
}

function discussion(vue) {
  if (!vue.discussion.length) return "";
  return `<ul class="discussion">${vue.discussion.map((message) => `
    <li><strong>${echapper(message.pseudo)}</strong> — ${echapper(message.texte)}</li>`)
    .join("")}</ul>`;
}

function ecranFinal(vue) {
  dessiner(`
    <h2>${echapper(vue.univers.textes.fin_titre)}</h2>
    <h1>${echapper(vue.resultat.camp)}</h1>
    <p class="sous-titre">${echapper(vue.resultat.texte)}</p>

    <h2>Qui était qui</h2>
    <ul class="village">
      ${vue.resultat.roles.map((ligne) => `<li>${echapper(ligne.pseudo)}
        <span class="voix">${echapper(ligne.role)}</span></li>`).join("")}
    </ul>

    <h2>Ce qui s'est passé</h2>
    ${journal(vue, vue.journal.length)}
    <button class="large" onclick="rejouer()">Une autre partie</button>
  `);
}

function rejouer() {
  sessionStorage.clear();
  window.location.href = "/";
}

/* ------------------------------------------------------- morceaux communs */

function journal(vue, combien) {
  const evenements = vue.journal.slice(-(combien || EVENEMENTS_AFFICHES));
  if (!evenements.length) return `<p class="patiente">Rien encore.</p>`;
  return `<ul class="journal">${evenements.map((evenement) => `
    <li><span class="quand">${echapper(evenement.quand)}</span>
      ${echapper(evenement.texte)}</li>`).join("")}</ul>`;
}

function mesSecrets(vue) {
  if (!vue.mes_revelations.length) return "";
  const lignes = vue.mes_revelations.slice(-3).map((secret) =>
    `<p>${echapper(secret.texte)}</p>`).join("");
  return `<h2>Ce que tu es seul à savoir</h2><div class="secret">${lignes}</div>`;
}

function consigne(vue) {
  // Un mort voit la partie continuer sans lui : son bandeau le dit.
  const classe = vue.moi.vivant ? "consigne" : "consigne bandeau";
  return `<p class="${classe}">${echapper(vue.instruction)}</p>`;
}

function minuterie(vue) {
  if (vue.secondes_restantes === null) return "";
  return `<p class="minuterie">${vue.secondes_restantes} s</p>`;
}

demarrer();
