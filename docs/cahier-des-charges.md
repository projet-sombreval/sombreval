# Cahier des charges — Projet Sombreval

Document de référence du projet. Il dit ce que le jeu doit faire, ce qu'il ne
fera pas, et pourquoi. En cas de désaccord pendant le développement, c'est ce
document qui tranche. Il se modifie comme le code : par une pull request.

## 1. Le besoin en trois phrases

Une classe de trente élèves, chacun chez soi devant son navigateur, veut jouer
ensemble à un jeu de déduction et de mensonge dans l'esprit du Loup-Garou.
Le jeu doit distribuer les rôles en secret, faire alterner les nuits et les
jours, compter les votes et annoncer le vainqueur, sans qu'un adulte ait à
tenir un carnet à la main.
Trois univers historiques sont proposés au choix : Sombreval 1348 (la peste),
Salem 1692 (les procès en sorcellerie), Sérénissime 1487 (Venise et ses
masques).

## 2. Les exigences

Chaque exigence est écrite du point de vue de quelqu'un. Trois personnes
existent dans ce projet :

- le **joueur** : un élève qui joue une partie ;
- le **meneur** : celui qui ouvre la partie et la fait avancer (un élève ou le
  professeur) ;
- le **professeur** : responsable de la séance et du serveur.

« Fini quand » est la définition de fini. Tant qu'une seule de ses lignes est
fausse, l'exigence n'est pas livrée. Chaque ligne doit pouvoir se vérifier en
regardant l'écran ou en lançant un test — pas en discutant.

---

### E1 — Ouvrir une partie

**En tant que** meneur, **je veux** ouvrir une nouvelle partie et obtenir un
code, **afin de** pouvoir le donner à la classe et que personne d'autre
n'entre.

Fini quand :
- un clic sur « Ouvrir une partie » affiche un code de 6 caractères ;
- deux parties ouvertes à la suite ont deux codes différents ;
- un code inconnu saisi par un joueur affiche « partie introuvable » et rien
  d'autre.

---

### E2 — Rejoindre une partie

**En tant que** joueur, **je veux** entrer un pseudo et un code de partie,
**afin de** rejoindre mes camarades sans créer de compte.

Fini quand :
- l'écran d'accueil demande deux choses et deux seulement : un pseudo et un
  code ;
- après validation, mon pseudo apparaît dans la liste des joueurs sur l'écran
  du meneur et sur celui des autres joueurs ;
- un pseudo déjà pris dans cette partie est refusé avec un message qui le dit ;
- un pseudo vide ou de plus de 20 caractères est refusé.

---

### E3 — Choisir l'univers

**En tant que** meneur, **je veux** choisir l'univers de la partie parmi les
trois proposés, **afin d'** adapter le décor et le nom des rôles à ce que la
classe a travaillé.

Fini quand :
- les trois univers (Sombreval 1348, Salem 1692, Sérénissime 1487) sont
  proposés avant le début de la partie ;
- l'univers choisi change le titre affiché, les couleurs de l'écran et le nom
  des rôles ;
- l'univers ne peut plus être changé une fois la partie commencée.

---

### E4 — Recevoir un rôle en secret

**En tant que** joueur, **je veux** recevoir un rôle que je suis le seul à
voir, **afin de** pouvoir mentir aux autres.

Fini quand :
- au démarrage, chaque joueur connecté reçoit exactement un rôle ;
- la répartition des rôles suit le tableau du nombre de joueurs (voir
  `roles/`) ;
- deux parties lancées avec les mêmes joueurs ne donnent pas la même
  distribution ;
- l'écran d'un joueur n'affiche jamais le rôle d'un autre joueur vivant ;
- un test vérifie que le rôle d'un joueur n'est pas envoyé aux autres.

---

### E5 — Consulter sa carte de personnage

**En tant que** joueur, **je veux** relire à tout moment la carte de mon
personnage, **afin de** me rappeler mon pouvoir sans redemander au meneur.

Fini quand :
- un bouton « Ma carte » est visible à toutes les phases ;
- la carte affichée est celle du dossier `cartes/` correspondant au rôle reçu ;
- la carte reste lisible sur un téléphone tenu à la verticale.

---

### E6 — Jouer la phase de nuit

**En tant que** joueur ayant un pouvoir, **je veux** agir pendant la nuit
pendant que les autres attendent, **afin d'** utiliser mon rôle sans que
personne ne sache ce que j'ai fait.

Fini quand :
- pendant la nuit, seuls les joueurs concernés voient un choix à faire ;
- les autres voient un écran d'attente sans information ;
- un joueur mort ne peut plus rien choisir ;
- la nuit se termine quand tous les joueurs concernés ont choisi, ou à la fin
  du temps imparti.

---

### E7 — Voter le jour

**En tant que** joueur vivant, **je veux** voter contre un autre joueur
vivant, **afin de** faire éliminer celui que je soupçonne.

Fini quand :
- chaque joueur vivant peut voter une fois et changer son vote tant que la
  phase dure ;
- un joueur mort ne peut pas voter et ne peut pas recevoir de vote ;
- le décompte affiché correspond aux votes réellement enregistrés ;
- en cas d'égalité, personne n'est éliminé et le message le dit clairement.

---

### E8 — Suivre l'état du village

**En tant que** joueur, **je veux** voir qui est vivant, qui est mort et ce qui
s'est passé, **afin de** raisonner comme autour d'une vraie table.

Fini quand :
- la liste des joueurs distingue visiblement les vivants des morts ;
- un journal affiche les événements publics dans l'ordre, avec le numéro du
  jour ;
- le journal ne contient aucune information secrète (ni rôle d'un vivant, ni
  auteur d'une action de nuit).

---

### E9 — Terminer la partie

**En tant que** joueur, **je veux** que le jeu annonce la fin et le camp
gagnant, **afin de** savoir quand c'est fini sans discussion.

Fini quand :
- la partie s'arrête dès qu'un camp remplit sa condition de victoire ;
- l'écran final nomme le camp gagnant et révèle le rôle de chaque joueur ;
- un test vérifie chaque condition de victoire sur une partie fabriquée pour
  l'occasion.

---

### E10 — Reprendre la main sur la partie

**En tant que** meneur, **je veux** pouvoir mettre en pause, passer une phase
ou arrêter la partie, **afin de** gérer une déconnexion ou la fin de l'heure.

Fini quand :
- trois boutons existent sur l'écran du meneur : pause, phase suivante, arrêt ;
- en pause, aucune action de joueur n'est enregistrée ;
- l'arrêt renvoie tous les joueurs à l'écran d'accueil.

---

### E11 — Ne rien laisser derrière soi

**En tant que** professeur, **je veux** qu'aucune donnée personnelle ne soit
conservée, **afin de** respecter le droit et de ne rien avoir à surveiller.

Fini quand :
- le jeu ne demande jamais ni nom, ni prénom, ni adresse électronique, ni
  photo ;
- les parties vivent en mémoire et disparaissent quand le serveur redémarre ;
- aucun fichier de partie n'est écrit sur le disque du serveur.

---

### E12 — Jouer depuis un téléphone

**En tant que** joueur, **je veux** jouer depuis mon téléphone, **afin de**
participer même sans ordinateur à la maison.

Fini quand :
- sur un écran de 360 pixels de large, aucun texte ne déborde et rien n'oblige
  à faire défiler horizontalement ;
- tous les boutons sur lesquels il faut appuyer font au moins 44 pixels de
  haut ;
- le jeu fonctionne dans Firefox et dans Chrome, sans rien installer.

## 3. Hors périmètre

Ces refus sont volontaires. Ils ne sont pas des oublis, et ce ne sont pas
non plus des « plus tard peut-être » : ce sont des décisions de conception.
**Les raisons comptent plus que les refus** — c'est le matériau de la
séance 2. Un refus dont on ne sait plus expliquer la raison est un refus à
rediscuter.

### Pas de classement entre joueurs

Pas de points, pas de podium, pas de statistiques par élève.
**Pourquoi :** le jeu repose sur le mensonge et l'élimination. Attacher un
score public à ça, dans une classe qui se retrouve le lendemain en cours,
transforme une partie en réputation durable. On veut que la partie se termine
quand elle se termine. Accessoirement, un classement suppose de reconnaître
les joueurs d'une partie à l'autre, ce qui suppose des comptes — voir le refus
suivant.

### Pas de comptes permanents

Un pseudo et un code de partie suffisent. Rien n'est enregistré entre deux
parties.
**Pourquoi :** les joueurs sont mineurs. Un compte, c'est une donnée
personnelle à collecter, à protéger, à conserver, à supprimer sur demande, et
un mot de passe oublié à réinitialiser un mardi à 8 h. Le coût juridique et
humain est sans rapport avec ce que le jeu y gagnerait. Sans compte, il n'y a
rien à fuiter.

### Pas d'application mobile

Le jeu s'ouvre dans un navigateur, à une adresse. Il n'y a rien à installer.
**Pourquoi :** une application veut dire deux développements (Android et iOS),
deux magasins d'applications, des comptes développeurs payants, une validation
qui prend des semaines et des élèves qui n'ont pas tous le droit d'installer
ce qu'ils veulent sur leur téléphone. L'exigence E12 obtient le même résultat
utile — jouer depuis un téléphone — pour le prix d'une feuille de style.

### Pas de chat vocal

La discussion du jour se fait par écrit dans le jeu, ou de vive voix par le
moyen que la classe utilise déjà.
**Pourquoi :** transmettre de la voix en direct entre trente personnes est un
problème d'ingénierie à part entière, et ce n'est pas celui qu'on apprend
ici. Surtout, une conversation vocale entre mineurs ne se modère pas et ne se
coupe pas facilement. Ce risque n'est pas à notre portée.

### Pas de reprise en cours de partie

On rejoint avant le début, pas après. Un joueur déconnecté peut revenir sur sa
place ; un joueur absent au lancement attend la partie suivante.
**Pourquoi :** les rôles sont distribués au démarrage en fonction du nombre de
joueurs. Ajouter quelqu'un après change cet équilibre et donne à l'arrivant
une information que les autres n'ont pas (il sait qui était déjà là). C'est
une règle de jeu avant d'être une limite technique.

### Pas de sauvegarde des parties

Une partie interrompue est perdue.
**Pourquoi :** sauvegarder suppose une base de données, donc une installation
sur le serveur du lycée, donc une autorisation, donc des données conservées.
Une séance dure une heure et une partie vingt minutes : le besoin n'existe
pas.

### Pas d'illustrations générées ni d'images sous droits

Les cartes de personnage sont faites en HTML et CSS, pas avec des images
trouvées en ligne.
**Pourquoi :** le dépôt est public. Toute image dont on ne peut pas prouver
l'origine est un problème de droit d'auteur pour le lycée. Et dessiner une
carte en CSS, c'est justement l'exercice des séances 2 à 4.

## 4. Les contraintes subies

Celles-là ne se discutent pas : elles viennent de l'extérieur du projet.

**Les joueurs sont mineurs.** Aucune donnée personnelle collectée, aucun
échange non modérable, aucun contenu venant de l'extérieur du dépôt. Cette
contrainte explique à elle seule la moitié de la section précédente.

**Le lycée est en ligne.** Les élèves jouent de chez eux, sur ce qu'ils ont :
un ordinateur familial, un téléphone, une connexion parfois mauvaise. Le jeu
doit supporter qu'un joueur disparaisse trente secondes et revienne. Rien ne
peut dépendre du fait que tout le monde est dans la même salle.

**Le serveur est celui du lycée.** Python 3 est disponible, la bibliothèque
standard aussi, et c'est tout. Pas d'installation de paquets, pas de base de
données, pas de service extérieur. Le serveur peut redémarrer sans prévenir —
d'où E11 et le refus de sauvegarde.

**La livraison est en mai.** La date est celle de la séance de jeu avec la
classe ; elle ne bouge pas. Ce qui bouge, c'est le contenu : si une exigence
n'est pas finie en avril, elle sort du périmètre de mai. On préfère un jeu
petit et qui marche à un jeu complet et cassé le jour J.
