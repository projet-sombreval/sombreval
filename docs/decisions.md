# Journal des décisions

Ce que nous avons décidé, quand, et pourquoi. Une décision qu'on ne sait
plus expliquer est une décision à rediscuter — c'est tout l'objet de ce
fichier.

Il complète [le cahier des charges](cahier-des-charges.md), qui dit ce que le
jeu doit faire. Ici, on dit comment, et pourquoi comme ça.

## Septembre 2026 — les sept décisions de la première tranche

**1. On invite par un lien, pas par un code.**
Le créateur ouvre une partie et envoie l'adresse. Rien à taper, rien à
épeler à voix haute, rien à recopier de travers depuis un tableau. La
connexion ne demande qu'un pseudonyme.
*Cette décision remplace les exigences E1 et E2 du cahier des charges, qui
parlaient d'un code à six caractères.*

**2. Le créateur choisit l'univers, une fois pour toutes.**
Les invités ne voient jamais l'écran de choix : ils arrivent en salle
d'attente et y découvrent où ils sont. Un seul univers par partie, sinon les
noms des rôles ne veulent plus rien dire.

**3. Le serveur décide, le navigateur affiche.**
Le rôle d'un joueur ne transite jamais vers les autres. Chaque joueur reçoit
une vue calculée pour lui seul. Ce qui n'est pas affiché n'est pas dans la
page : on peut ouvrir l'inspecteur du navigateur en pleine partie, il n'y a
rien à y trouver. C'est vrai dès la première démonstration, même avec des
joueurs factices — c'est la règle qu'on montre, pas celle qu'on promet.

**4. Un seul moteur, réglé par des fichiers.**
Aucun nom de rôle, aucun texte, aucune couleur n'est écrit dans le code.
`regles/roles.yaml` décrit la mécanique, commune aux trois univers ;
`regles/univers/<nom>.yaml` décrit les noms et les textes. Ajouter un rôle
ou un univers doit être une ligne de configuration, pas une modification du
moteur. C'est aussi ce qui permet à un élève de contribuer sans savoir
programmer.

*Précisé le 29 octobre 2026.* La règle porte sur la **fiction du monde** —
les noms, les textes et les couleurs d'un univers, ce qui fait qu'il est
Salem plutôt que Sérénissime. Elle ne porte **pas** sur les libellés de
l'interface, qui restent dans le code : « Le village », « Ce qui s'est
passé », « Fermer », les phrases de la carte d'un joueur. Le critère tient
en une question : **ce texte serait-il différent dans un autre monde ?** Si
oui, il appartient au fichier de l'univers ; sinon, à l'écran. Faire remonter
un libellé d'interface dans les trois fichiers d'univers n'y ajouterait que
trois « à écrire » identiques, sans rien à inventer.

**5. La nuit est un seul écran, identique pour tous.**
Seul le texte de l'instruction change selon le rôle. Tout le monde joue en
même temps : pas d'ordre de réveil, pas d'attente de son tour. Un jeu où
sept personnes sur huit regardent un écran d'attente pendant deux minutes
n'est pas un jeu.

**6. Le rôle d'un joueur éliminé est révélé immédiatement.**
Sans révélation, un vote raté ne s'apprend jamais et le village raisonne
dans le vide. C'est une règle de jeu, pas une facilité technique.

**7. La discussion se fait par phrases toutes faites.**
Jamais de saisie libre. Les joueurs sont mineurs, le jeu se joue à distance
et personne ne peut modérer trente conversations en direct. Les phrases sont
dans le fichier de l'univers ; les rajouter est un travail d'élève.

## Octobre 2026 — l'hébergement

**8. Le jeu est hébergé dans un conteneur isolé, sur un sous-domaine dédié.**
Un conteneur à lui, géré comme les autres applications de la plateforme, à son
adresse. Trois raisons, et la troisième est la seule qui ait vraiment tranché.

D'abord, **il n'y a rien à protéger qui ne le soit déjà** : aucune donnée
personnelle n'est conservée (E11), aucune saisie n'est libre (décision 7),
aucune base de données n'existe. Le serveur fait cent lignes et ne contient
aucune règle du jeu ; tout le moteur se teste sans lui.

Ensuite, **le secret des rôles reste tenu côté serveur**, exactement comme le
dit la décision 3 : la vue de chaque joueur est calculée pour lui seul. Un
hébergement ne change pas cette propriété — c'est le moteur qui la tient, pas
l'endroit où il tourne.

Enfin, **l'API ne peut pas vivre sur des pages statiques.** `site/js/jeu.js`
appelle `/api/…` en chemins relatifs, et c'est `jeu/serveur.py` qui monte
`site/` à la racine : servi par un hébergement de fichiers statiques, le jeu
s'affiche et répond 404 à sa première requête. Il faut donc un serveur qui
tourne, et c'est ce qui fixe la date.

⚠️ **Un point à ne pas oublier au provisionnement** : `jeu/serveur.py` écoute
aujourd'hui `host="127.0.0.1"`, c'est-à-dire la boucle locale **uniquement**.
Dans un conteneur, personne ne peut l'atteindre de l'extérieur : il devra
écouter l'interface du conteneur. C'est la panne silencieuse classique — le
serveur démarre, les journaux sont propres, et l'adresse ne répond pas. À
changer **avec** le provisionnement, pas avant : en local, `127.0.0.1` est le
bon réglage.

## Ce que la première tranche ne fait pas

Il fallait quelque chose qui tourne pour la séance de lancement du
21 septembre 2026, en trois minutes, devant une classe. Le reste attendra :

- **pas de vrai multijoueur** : les sept autres joueurs sont joués par le
  programme, avec des choix simples et au hasard. Ils passent par les mêmes
  vérifications que les humains — ils ne trichent pas ;
- **pas de temps réel, pas de base de données** : l'état des parties vit en
  mémoire et disparaît au redémarrage du serveur. Ça suffit pour une séance,
  et ça respecte l'exigence E11 (ne rien laisser derrière soi) ;
- **pas de contenu pour Salem ni Sérénissime** : les deux univers existent,
  s'affichent en « bientôt », et refusent de se lancer ;
- **cinq rôles sur dix sont jouables** : les cinq autres sont décrits dans
  `regles/roles.yaml` avec `implemente: false`. Le jeu refuse de lancer une
  partie qui en contient un, plutôt que de se bloquer en pleine séance.

## Les réglages de démonstration

Deux réglages de `regles/partie.yaml` existent pour la classe, et pas pour
le jeu :

- `durees` : dix secondes par phase. On ne peut pas faire attendre trois
  minutes un vote en direct. Pour une vraie partie, il faudra remonter à une
  ou deux minutes ;
- `role_du_createur` : force le rôle de celui qui ouvre la partie, pour
  pouvoir répéter la démonstration. **À remettre à `null` dès que la classe
  jouera pour de vrai** : un rôle imposé, c'est une partie truquée.
