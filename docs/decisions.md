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

## Mise à jour du 15 septembre 2026 — la séance de lancement

La séance du 21 septembre se jouera finalement sur <https://wolfy.fr>, un
Loup-Garou en ligne qui existe déjà : la classe découvre le genre en y
jouant, et notre jeu n'est pas montré ce jour-là.

Ce qui précède n'est pas effacé pour autant : c'est la raison pour laquelle
la première tranche a été faite comme ça, et la contrainte des trois minutes
a produit un jeu qui tourne pour de bon plutôt qu'une maquette. Le scénario
de démonstration est rangé dans [demonstration.md](demonstration.md), pour
le jour où on montrera le jeu.

## Les réglages de démonstration

Deux réglages de `regles/partie.yaml` existent pour la classe, et pas pour
le jeu :

- `durees` : dix secondes par phase. On ne peut pas faire attendre trois
  minutes un vote en direct. Pour une vraie partie, il faudra remonter à une
  ou deux minutes ;
- `role_du_createur` : force le rôle de celui qui ouvre la partie, pour
  pouvoir répéter la démonstration. **À remettre à `null` dès que la classe
  jouera pour de vrai** : un rôle imposé, c'est une partie truquée.
