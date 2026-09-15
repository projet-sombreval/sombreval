# Montrer le jeu en trois minutes

Ce document n'est pas pour la séance de lancement. Le 21 septembre 2026, la
classe découvre le genre en jouant à un Loup-Garou en ligne qui existe déjà,
<https://wolfy.fr> (l'adresse renvoie sur wolfy.net) : on joue à ce qu'on va
fabriquer avant de le fabriquer, et rien ne peut rater.

Ce qui suit sert pour le jour où on montrera **notre** jeu — une séance plus
tard, une porte ouverte, un conseil de classe. C'est la suite exacte des
clics et ce qu'il y a à dire à chaque écran. Le jeu tourne vraiment : voir
« Lancer le jeu » dans le [README](../README.md).

À lire tel quel : la colonne de droite est ce qu'il y a à dire.

**Avant de commencer**, vérifie deux choses dans `regles/partie.yaml` :
`role_du_createur: enqueteur` (tu auras le Bailli à coup sûr, le rôle qui
montre le mieux le jeu) et `durees` à 10 secondes. Lance le serveur, ouvre
<http://localhost:8000>, et n'entre pas encore ton pseudonyme.

| Écran | Ce que tu fais | Ce que tu dis |
|---|---|---|
| **1. Accueil** | Tu montres l'écran, tu tapes `Delphine`, tu cliques sur **Entrer**. | « Voilà le jeu qu'on va fabriquer cette année. Un village, une menace cachée, et personne ne sait qui est qui. On ne demande qu'un pseudonyme : pas de compte, pas de mot de passe, pas d'adresse. » |
| **2. Les trois villages** | Tu montres les trois, tu cliques sur **Sombreval 1348**. | « Trois univers, trois époques. Deux ne sont pas encore écrits — vous les écrirez. Et pourtant, il n'y aura qu'un seul programme : ce qui change entre Salem et Sombreval, c'est un fichier de texte, pas une ligne de code. » |
| **3. Salle d'attente** | Tu montres le lien, puis la liste qui se remplit toute seule. | « Pour inviter quelqu'un, on envoie ce lien. C'est tout. Là, les sept autres joueurs sont joués par le programme — je suis seule devant mon écran, mais le jeu ne le sait pas : ils passent par les mêmes règles que moi. » |
| **4. Ton rôle** | Tu cliques sur **Commencer la partie**. Le rôle s'affiche : le Bailli. | « Voilà mon rôle. Moi seule le vois. » |
| **4 bis. La preuve** | `F12` → onglet **Réseau** → clique sur la ligne `vue` → **Réponse**. Montre la liste `joueurs`. | « Voici exactement ce que mon navigateur a reçu du serveur. Regardez la liste des joueurs : des pseudonymes, et pas un seul rôle. Le rôle des autres n'est pas caché dans la page — il n'y est pas. C'est le serveur qui décide de ce que chacun a le droit de savoir. C'est la règle numéro un du projet. » |
| **5. La nuit** | Tu choisis quelqu'un à sonder. Tu laisses le compte à rebours finir. | « La nuit, tout le monde joue en même temps, sur le même écran : seule l'instruction change. Moi, je peux sonder un habitant. Dix secondes, parce que je ne peux pas vous faire attendre — c'est un réglage, pas une loi. » |
| **6. Le jour** | Tu montres le journal en haut, puis tu cliques une phrase, puis un nom. | « Au matin, le village apprend qui est mort, et son rôle. On discute — mais avec des phrases toutes faites : personne n'écrit ce qu'il veut, c'est voulu. Puis on vote. Regardez en bas à droite : ce que j'ai appris cette nuit, moi seule le vois. » |
| **7. Le vote tombe** | Tu attends la fin du compte à rebours. | « Les autres votent à la fin du temps, souvent comme moi. Une égalité n'élimine personne. » |
| **8. On recommence** | Tu laisses tourner une nuit et un jour de plus, sans commenter. | « Et ça tourne comme ça jusqu'à ce qu'un camp gagne. » |
| **9. La fin** | L'écran final. | « Le village a gagné, ou les loups. Et on découvre enfin qui était qui. Voilà. Trois minutes. Il reste à écrire les neuf autres rôles, deux univers, et les cartes de personnage — c'est vous qui allez le faire. » |

**Si la partie s'éternise** (ça arrive quand tu ne votes pas), commente
pendant les tours en trop, ou recharge la page pour repartir.

**Si tu es éliminée en route**, ne t'excuse pas : c'est un écran prévu.
« Je suis morte. Je vois tout, je ne vote plus, je ne parle plus, et la
partie continue sans moi. » Puis tu montres l'écran final.
