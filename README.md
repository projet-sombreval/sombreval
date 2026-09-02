# Sombreval

Le jeu de rôle en ligne de l'option **Projet Sombreval**.

Un jeu de déduction et de mensonge dans l'esprit du Loup-Garou, joué dans le
navigateur : le jeu distribue les rôles en secret, fait alterner les nuits et
les jours, compte les votes et annonce le vainqueur. Trois univers historiques
au choix du meneur :

| Univers | Année | Le décor |
|---|---|---|
| **Sombreval** | 1348 | La peste remonte la vallée. |
| **Salem** | 1692 | Le village accuse, le tribunal écoute. |
| **Sérénissime** | 1487 | Venise complote derrière ses masques. |

La partie se jouera en mai avec la classe. D'ici là, le dépôt sert aussi de
support de cours : tout ce qu'il contient est écrit pour être lu par des
débutants.

## Lancer le jeu en local

Il faut Python 3 — rien d'autre à installer. Depuis le dossier du dépôt :

```bash
cd sombreval
python3 -m jeu.serveur
```

Puis ouvre <http://localhost:8000> dans ton navigateur. `Ctrl-C` arrête le
serveur.

Si tu n'as pas encore le dépôt sur ta machine :

```bash
git clone https://github.com/projet-sombreval/sombreval.git
```

## Lancer les tests

```bash
python3 -m unittest discover tests
```

## Le dépôt

| Dossier | Ce qu'il contient |
|---|---|
| [`jeu/`](jeu/) | Le code du jeu : les règles et le serveur local. |
| [`site/`](site/) | Les écrans vus par les joueurs (HTML et CSS). |
| [`docs/`](docs/) | Le [cahier des charges](docs/cahier-des-charges.md) : ce que le jeu doit faire, et ce qu'il ne fera pas. |
| [`cartes/`](cartes/) | **Le dossier des élèves** : une carte de personnage par élève. Voir [son mode d'emploi](cartes/README.md). |
| [`roles/`](roles/) | Les fiches techniques des rôles, rangées par univers. Fiche de référence : [le bailli](roles/sombreval/bailli.md). |
| [`tests/`](tests/) | Les tests automatiques. |

## Contribuer

Une tâche, une branche, une pull request relue — et jamais rien directement
sur `main`. Tout est expliqué dans [CONTRIBUTING.md](CONTRIBUTING.md).

## Licence

MIT — voir [LICENSE](LICENSE).
