# Sombreval

Le jeu de rôle en ligne de l'option **Projet Sombreval**.

Un jeu de déduction et de mensonge dans l'esprit du Loup-Garou, joué dans le
navigateur : le serveur distribue les rôles en secret, fait alterner les
nuits et les jours, compte les votes et annonce le vainqueur. Trois univers
historiques, un seul moteur :

| Univers | Année | Le décor | État |
|---|---|---|---|
| **Sombreval** | 1348 | La peste remonte la vallée. | jouable |
| **Salem** | 1692 | Le village accuse, le tribunal écoute. | bientôt |
| **Sérénissime** | 1487 | Venise complote derrière ses masques. | bientôt |

La partie se jouera en mai avec la classe. D'ici là, le dépôt sert aussi de
support de cours : tout ce qu'il contient est écrit pour être lu par des
débutants.

## Lancer le jeu

Il faut Python 3. Le jeu a besoin de deux bibliothèques, qu'on installe dans
un dossier `.venv` à part, sans rien changer au reste de la machine.

**La première fois, et une seule fois**, depuis le dossier du dépôt :

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

**Ensuite, à chaque fois**, dans un terminal neuf :

```bash
source .venv/bin/activate
python3 -m jeu.serveur
```

Puis ouvre <http://localhost:8000>. `Ctrl-C` arrête le serveur.

Deux choses qui peuvent coincer :

- `python3 -m pip` répond **« No module named pip »** : c'est normal, et
  c'est pour ça qu'on passe par `.venv` — pip n'est pas installé sur la
  machine, mais chaque `.venv` en contient un. Suis les commandes ci-dessus.
- `python3 -m venv .venv` répond **« ensurepip is not available »** : il
  manque un paquet du système, à installer une fois avec
  `sudo apt install python3.12-venv`.

Le dossier `.venv` n'est pas suivi par git : il t'appartient, il se refait en
deux commandes, et on peut le supprimer sans rien casser.

## Scénario de démonstration

Trois minutes, en partage d'écran, devant des élèves qui ne connaissent rien
au projet. À lire tel quel — la colonne de droite est ce qu'il y a à dire.

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

## Ce que fait cette tranche, et ce qu'elle ne fait pas

Elle fait : une partie complète à 8 joueurs dans l'univers de Sombreval,
du lien d'invitation à l'écran final, avec cinq rôles (le Loup, le Bailli,
le Chevalier, l'Herboriste, le Manant).

Elle ne fait pas — et c'est volontaire : pas de vrai multijoueur (les sept
autres joueurs sont le programme), pas de comptes, pas de base de données
(tout est en mémoire et disparaît au redémarrage), pas de contenu pour Salem
ni Sérénissime, pas de modération, pas de sauvegarde.

Les décisions de conception et leurs raisons sont dans
[docs/decisions.md](docs/decisions.md) ; le besoin et les exigences dans
[docs/cahier-des-charges.md](docs/cahier-des-charges.md).

## Comment c'est fait

**Le serveur décide, le navigateur affiche.** Le rôle d'un joueur ne part
jamais vers les autres navigateurs. Chaque joueur reçoit une vue filtrée,
calculée dans [jeu/vues.py](jeu/vues.py) : ce qui n'est pas affiché n'est pas
non plus dans la page. On peut ouvrir l'inspecteur, il n'y a rien à y
trouver.

**Un seul moteur, réglé par des fichiers.** Aucun nom de rôle, aucun texte,
aucune couleur n'est écrit dans le code :

| Fichier | Ce qu'il décide |
|---|---|
| [regles/roles.yaml](regles/roles.yaml) | Les dix rôles : leur camp, leur action, quand ils agissent. Et les compositions selon le nombre de joueurs. |
| [regles/univers/sombreval.yaml](regles/univers/sombreval.yaml) | Les noms, les textes, les couleurs, les phrases de la discussion. |
| [regles/partie.yaml](regles/partie.yaml) | Les durées, le nombre de joueurs, les réglages de démonstration. |

Cinq rôles sur dix sont joués par le moteur ; les cinq autres sont décrits
avec `implemente: false`, et le jeu refuse de lancer une partie qui en
contient un plutôt que de se bloquer en pleine séance.

**La nuit est résolue dans un ordre fixe**, côté serveur, et c'est le
morceau le plus délicat du jeu : on fige l'état, on applique les
protections, puis les éliminations, puis on calcule les révélations sur
l'état figé. Tout est dans [jeu/nuit.py](jeu/nuit.py), avec l'explication
de pourquoi cet ordre-là.

## Lancer les tests

```bash
python3 -m unittest discover tests
```

Ils ne demandent ni serveur ni bibliothèque : tout le jeu se teste sans le
web, parce que [jeu/application.py](jeu/application.py) ne connaît pas HTTP.

## Le dépôt

| Dossier | Ce qu'il contient |
|---|---|
| [`jeu/`](jeu/) | Le code : les règles, la vue filtrée, les joueurs factices, le serveur. |
| [`regles/`](regles/) | Les fichiers de configuration lus par le moteur. |
| [`site/`](site/) | Les écrans vus par les joueurs (HTML, CSS, JavaScript). |
| [`docs/`](docs/) | Le cahier des charges et le journal des décisions. |
| [`cartes/`](cartes/) | **Le dossier des élèves** : une carte de personnage par élève. Voir [son mode d'emploi](cartes/README.md). |
| [`roles/`](roles/) | Les fiches de rôle, en français, rangées par univers. À ne pas confondre avec `regles/`, que lit le programme. |
| [`tests/`](tests/) | Les tests automatiques. |

## Contribuer

Une tâche, une branche, une pull request relue — et jamais rien directement
sur `main`. Tout est expliqué dans [CONTRIBUTING.md](CONTRIBUTING.md).

## Licence

MIT — voir [LICENSE](LICENSE).
