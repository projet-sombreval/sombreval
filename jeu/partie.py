"""Une partie : ses joueurs, sa phase, son état.

Cet objet ne décide rien tout seul. Ce sont les modules nuit.py, jour.py et
phases.py qui le font avancer. Ici, on ne trouve que l'état et les questions
qu'on lui pose (« qui est vivant ? », « qui joue ce rôle ? »).
"""

import random
import secrets

from jeu.erreurs import ErreurDeJeu

LONGUEUR_MAX_DU_PSEUDO = 20


class Joueur:
    """Un joueur, humain ou factice.

    Deux identités, et c'est important :
    - le numéro est public (« j3 ») : il circule dans les pages ;
    - le jeton est secret : il prouve qui tu es et n'est jamais envoyé aux
      autres joueurs.
    """

    def __init__(self, numero, pseudo, automate=False):
        self.numero = numero
        self.jeton = secrets.token_urlsafe(16)
        self.pseudo = pseudo
        self.automate = automate
        self.role = None
        self.vivant = True


class Partie:

    def __init__(self, identifiant, univers, configuration, hasard=None):
        self.identifiant = identifiant
        self.univers = univers
        self.configuration = configuration
        self.hasard = hasard or random.Random()

        self.joueurs = []
        self.createur = None
        self.phase = "attente"
        self.fin_de_phase = None
        self.numero_de_nuit = 0
        self.derniere_arrivee = None

        # Ce que les joueurs ont choisi pendant la phase en cours.
        self.actions_de_nuit = {}      # numéro -> numéro visé
        self.votes = {}                # numéro -> numéro visé
        self.discussion = []           # les messages du jour
        self.retardataires = []        # les automates qui votent en dernier

        # Ce que le jeu retient d'une phase à l'autre.
        self.journal = []              # les événements publics
        self.revelations = {}          # numéro -> ce que lui seul a appris
        self.cible_precedente = {}     # numéro -> qui il a visé la nuit d'avant
        self.pouvoirs_utilises = set() # ceux qui ont grillé leur unique usage
        self.camp_gagnant = None

    # --- questions simples -------------------------------------------------

    def vivants(self):
        return [joueur for joueur in self.joueurs if joueur.vivant]

    def joueur_par_jeton(self, jeton):
        for joueur in self.joueurs:
            if joueur.jeton == jeton:
                return joueur
        raise ErreurDeJeu("Tu n'es pas dans cette partie.")

    def joueur_par_numero(self, numero):
        for joueur in self.joueurs:
            if joueur.numero == numero:
                return joueur
        raise ErreurDeJeu("Ce joueur n'existe pas.")

    def camp_de(self, joueur):
        return self.configuration.role(joueur.role)["camp"]

    def joueurs_du_camp(self, camp):
        return [j for j in self.joueurs if self.camp_de(j) == camp]

    def nom_du_role(self, joueur):
        """Le nom du rôle dans l'univers choisi : « le Bailli »."""
        return self.univers["roles"][joueur.role]["nom"]

    def texte(self, cle, **remplacements):
        """Un texte de l'univers, avec ses trous remplis."""
        return self.univers["textes"][cle].format(**remplacements)

    def texte_du_role(self, joueur, cle, **remplacements):
        """Un texte rangé avec le rôle : son instruction, sa confirmation.

        Renvoie None si l'univers n'a pas prévu ce texte-là pour ce rôle :
        un rôle qui ne révèle rien n'a pas de texte de révélation.
        """
        modele = self.univers["roles"][joueur.role].get(cle)
        return modele.format(**remplacements) if modele else None

    def noter_au_journal(self, texte):
        self.journal.append({"quand": self._moment(), "texte": texte})

    def noter_pour(self, joueur, texte):
        """Une information privée : elle n'ira que dans SA vue."""
        self.revelations.setdefault(joueur.numero, []).append(
            {"quand": self._moment(), "texte": texte}
        )

    def _moment(self):
        """« Nuit 3 » ou « Jour 3 » — les mots viennent de l'univers."""
        cle = "nuit_numero" if self.phase == "nuit" else "jour_numero"
        return self.texte(cle, numero=self.numero_de_nuit)


def ajouter_un_joueur(partie, pseudo, automate=False):
    """Fait entrer un joueur en salle d'attente."""
    if partie.phase != "attente":
        raise ErreurDeJeu("La partie a déjà commencé.")

    pseudo = pseudo.strip()
    if not pseudo:
        raise ErreurDeJeu("Il faut un pseudonyme.")
    if len(pseudo) > LONGUEUR_MAX_DU_PSEUDO:
        raise ErreurDeJeu(
            f"Le pseudonyme fait plus de {LONGUEUR_MAX_DU_PSEUDO} lettres."
        )
    if any(j.pseudo.lower() == pseudo.lower() for j in partie.joueurs):
        raise ErreurDeJeu("Ce pseudonyme est déjà pris dans cette partie.")
    if len(partie.joueurs) >= partie.configuration.parametres["nombre_de_joueurs"]:
        raise ErreurDeJeu("La partie est complète.")

    joueur = Joueur(f"j{len(partie.joueurs) + 1}", pseudo, automate)
    partie.joueurs.append(joueur)
    if partie.createur is None:
        partie.createur = joueur.numero
    return joueur


def distribuer_les_roles(partie):
    """Donne un rôle à chaque joueur, au hasard.

    Le réglage « role_du_createur » sert à répéter la démonstration : il
    force le rôle de celui qui a ouvert la partie. Vide, tout est tiré au
    sort.
    """
    composition = partie.configuration.composition(len(partie.joueurs))

    a_distribuer = []
    for nom, combien in composition.items():
        a_distribuer.extend([nom] * combien)

    joueurs = list(partie.joueurs)
    impose = partie.configuration.parametres.get("role_du_createur")
    if impose:
        if impose not in a_distribuer:
            raise ErreurDeJeu(
                f"Le rôle imposé « {impose} » n'est pas dans la composition."
            )
        createur = partie.joueur_par_numero(partie.createur)
        createur.role = impose
        a_distribuer.remove(impose)
        joueurs.remove(createur)

    partie.hasard.shuffle(a_distribuer)
    for joueur, role in zip(joueurs, a_distribuer):
        joueur.role = role
