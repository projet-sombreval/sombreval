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

## Montrer le jeu

La séance de lancement du 21 septembre 2026 ne fait pas tourner ce jeu-ci :
la classe joue à <https://wolfy.fr>, un Loup-Garou en ligne qui existe déjà,
pour découvrir le genre avant de le fabriquer.

Pour le jour où on montrera **notre** jeu, le scénario complet — la suite des
clics et ce qu'il y a à dire à chaque écran — est dans
[docs/demonstration.md](docs/demonstration.md).

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
