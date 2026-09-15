# En vrai — quoi ouvrir au troisième temps de chaque séance

Le troisième temps de séance, c'est le moment où les élèves voient le vrai
code du projet. Ce document dit quoi ouvrir, dans quel ordre, et quoi faire
remarquer — pour ne rien chercher en direct devant eux.

La séance de lancement fait exception : on n'y ouvre rien du dépôt, et notre
jeu ne tourne pas. Elle est quand même dans le tableau, pour que le tableau
dise tout.

## Le tableau de correspondance

| Séance | Sujet | Ce que j'ouvre | Ça existe ? |
|---|---|---|---|
| **S1** — 21/09 | Découvrir le genre | Rien du dépôt : la classe joue à <https://wolfy.fr> | **Sans objet.** Notre jeu ne tourne pas ce jour-là. Voir la séance 1 ci-dessous. |
| **S2** — 28/09 | HTML sémantique | `cartes/exemple-bailli.html` (la carte de référence) **et** `site/js/jeu.js` (l'écran de rôle du jeu) | **Oui, mais pas comme prévu.** L'écran de découverte du rôle n'existe pas en HTML : il est fabriqué en JavaScript, et il a **moins** de balises que la carte des élèves. Voir la séance 2 ci-dessous. |
| **S3** — 05/10 | CSS et variables d'univers | `cartes/exemple-bailli.css` (instantané) puis `regles/univers/sombreval.yaml` (le vrai réglage du jeu) | **Oui**, mais la valeur qui fait basculer l'ambiance du jeu n'est pas dans le CSS : elle est dans le YAML. C'est justement la leçon. |
| **S4** — 12/10 | Responsive et clavier | `site/css/site.css` et n'importe quel écran du jeu | **Le responsive : oui.** **Le clavier : non.** La page est redessinée entièrement chaque seconde, donc le focus du clavier est perdu chaque seconde. Voir la séance 4. |

---

## S1 — 21/09 — découvrir le genre

On ne montre pas le jeu du dépôt : la classe joue à un Loup-Garou en ligne
qui existe déjà. On joue à ce qu'on va fabriquer avant de le fabriquer, et
rien ne peut rater en direct.

| | |
|---|---|
| **Adresse** | <https://wolfy.fr> — l'adresse renvoie sur `wolfy.net`, c'est normal |
| **Fichier du dépôt** | aucun |
| **Commande** | aucune : notre serveur reste éteint |

> **Ce que je fais remarquer :** tout ce qui se passe là — le rôle qu'on
> reçoit en secret, la nuit où l'on agit sans se voir, le vote du jour, le
> mort dont on révèle le rôle — c'est exactement la liste de ce que vous
> aurez à écrire ; et ce qui vous manque ou vous agace en jouant, notez-le,
> c'est la matière de la séance 2.

Le scénario pour montrer **notre** jeu, le jour où ce sera le moment, est
dans [demonstration.md](demonstration.md).

---

## S2 — 28/09 — HTML sémantique

### Ce qu'il faut savoir avant d'entrer en classe

Tu voulais montrer « la vraie carte » à côté de celle des élèves, et dire
pourquoi elle contient plus de balises. **Ça ne marche pas avec l'écran du
jeu, et il vaut mieux le savoir maintenant :**

| | Balises différentes dans le corps de la page |
|---|---|
| `cartes/exemple-bailli.html` | **11** : `article`, `header`, `h1`, `section`, `h2`, `dl`, `dt`, `dd`, `p`, `strong`, `footer` |
| L'écran de rôle du jeu | **3** : `h2`, `div`, `p` |

L'écran de rôle du jeu est donc *moins* sémantique que la carte de tes
élèves. C'est un défaut réel du dépôt, pas un piège pédagogique — mais il
fait une très bonne séance : ils viennent d'écrire mieux que le jeu.

### Ce que j'ouvre

| | |
|---|---|
| **Fichier 1 — la référence** | `cartes/exemple-bailli.html` |
| **URL GitHub** | https://github.com/projet-sombreval/sombreval/blob/main/cartes/exemple-bailli.html |
| **URL locale** | `file:///home/delf/projets/sombreval/cartes/exemple-bailli.html` — depuis un navigateur Windows : `file://wsl.localhost/Ubuntu/home/delf/projets/sombreval/cartes/exemple-bailli.html` |
| **Commande** | aucune : c'est un fichier, il s'ouvre tout seul. |
| **Fichier 2 — le jeu** | `site/js/jeu.js`, fonction `ecranDecouverteDuRole` (ligne 267) |
| **URL GitHub** | https://github.com/projet-sombreval/sombreval/blob/main/site/js/jeu.js#L267-L279 |
| **Commande** | `python3 -m jeu.serveur` |
| **URL locale** | http://localhost:8000 — l'écran de rôle apparaît juste après « Commencer la partie » |

> **Ce que je fais remarquer :** la carte des élèves annonce à la machine ce
> que chaque morceau *est* (`header` l'en-tête, `dl`/`dt`/`dd` une liste de
> questions-réponses, `footer` le pied), alors que l'écran du jeu n'a que
> des `div` et des `p` qui ne disent rien — et c'est le jeu qui a tort.

**Pour garder l'écran de rôle affiché** : il ne dure que 8 secondes. Avant
de lancer le serveur, mets `decouverte_du_role: 300` dans
`regles/partie.yaml`, et `delai_entre_les_arrivees: 0.1` pour que le village
se remplisse tout de suite. Suite exacte des clics : pseudonyme → **Entrer**
→ **Sombreval 1348** → attendre que le village soit à 8 → **Commencer la
partie**.

**Ce qu'ils peuvent faire ensuite** (une issue toute prête) : réécrire
`ecranDecouverteDuRole` avec `article`, `header`, `h1` et `dl`, en repartant
de leur propre carte.

---

## S3 — 05/10 — CSS et variables d'univers

### Ce qu'il faut savoir avant d'entrer en classe

`site/css/site.css` **ne contient aucune couleur de Sombreval**. Les sept
valeurs du bloc `:root` (ligne 10) sont des gris neutres de secours. Les
vraies couleurs sont dans `regles/univers/sombreval.yaml` : le serveur les
envoie au navigateur, qui les pose comme variables CSS
(`appliquerLesCouleurs`, `site/js/jeu.js` ligne 69).

Donc si tu changes une valeur dans `site.css` en direct, **il ne se passera
rien** : la valeur du YAML l'écrase une fois par seconde. Fais-le une fois
exprès, c'est la démonstration la plus parlante de la séance.

### Ce que j'ouvre

| | |
|---|---|
| **D'abord — leur fichier** | `cartes/exemple-bailli.css`, ligne 18 : `--accent: #7d1f13;` |
| **URL GitHub** | https://github.com/projet-sombreval/sombreval/blob/main/cartes/exemple-bailli.css#L13-L46 |
| **URL locale** | `file:///home/delf/projets/sombreval/cartes/exemple-bailli.html` |
| **Le geste** | remplace `#7d1f13` par `#2f4858`, enregistre, `F5` : toute la carte bascule. Puis montre qu'il existe déjà trois palettes complètes dans le même fichier (`.univers-sombreval` ligne 13, `.univers-salem` ligne 27, `.univers-serenissime` ligne 38) et qu'il suffit de changer la classe du `<body>`. |
| **Ensuite — le jeu** | `regles/univers/sombreval.yaml`, ligne 25 : `accent: "#8d2119"` |
| **URL GitHub** | https://github.com/projet-sombreval/sombreval/blob/main/regles/univers/sombreval.yaml#L20-L27 |
| **Commande** | `python3 -m jeu.serveur` |
| **URL locale** | http://localhost:8000 |
| **Le geste** | change la valeur, puis `Ctrl-C` et relance le serveur, puis `F5` dans le navigateur : le fichier de règles n'est lu qu'au démarrage. Pour un changement instantané devant la classe, fais-le plutôt dans l'inspecteur : `F12` → **Éléments** → la balise `<html>` → panneau **Styles** → `--accent`. |

> **Ce que je fais remarquer :** une couleur écrite une seule fois et
> réutilisée partout par son nom, c'est une variable — et dans le jeu elle
> n'est même pas dans le CSS, parce qu'un fichier de couleurs est du décor,
> pas du programme : c'est ce qui permettra d'écrire Salem sans toucher au
> code.

---

## S4 — 12/10 — Responsive et clavier

### Ce qu'il faut savoir avant d'entrer en classe

**La moitié « responsive » marche.** Il y a une seule *media query* dans
tout le dépôt (`site/css/site.css` ligne 140) : à moins de 480 pixels, la
grille des joueurs passe de deux colonnes à une seule. Vérifié à 360
pixels : rien ne déborde, les boutons font au moins 48 pixels de haut.

**La moitié « clavier » ne marche pas, et c'est un vrai défaut.** Pendant
une partie, le navigateur redemande son écran au serveur toutes les
secondes et réécrit toute la page (`dessiner`, `site/js/jeu.js` ligne 25).
Chaque réécriture détruit l'élément qui avait le focus : tu appuies sur
`Tab` trois fois, tu attends une seconde, et tu repars du haut. Il n'y a
pas non plus de style de focus défini — on voit celui du navigateur, par
défaut.

Deux écrans échappent à ça, parce qu'ils sont affichés avant que la boucle
démarre : **l'accueil** et **le choix de l'univers**. C'est là qu'il faut
faire la démonstration au clavier.

### Ce que j'ouvre

| | |
|---|---|
| **Fichier** | `site/css/site.css` — `@media (min-width: 30rem)` ligne 140, et `button` ligne 98 |
| **URL GitHub** | https://github.com/projet-sombreval/sombreval/blob/main/site/css/site.css#L131-L150 |
| **Commande** | `python3 -m jeu.serveur` |
| **URL locale** | http://localhost:8000 |

**Suite exacte des gestes :**

1. **Le responsive** — sur l'écran du jour, `F12` → l'icône de téléphone en
   haut de l'inspecteur → largeur **360** : la grille passe à une colonne.
   Remonte à **500** : elle repasse à deux. La bascule est à 480.
2. **Le clavier qui marche** — recharge la page pour revenir à l'accueil,
   range la souris, et fais tout au clavier : `Tab` jusqu'au champ,
   tape un pseudonyme, `Tab`, `Entrée`, puis `Tab` entre les trois univers
   et `Entrée` sur Sombreval.
3. **Le clavier qui casse** — une fois la partie lancée, refais `Tab` trois
   fois et attends. Le focus disparaît. C'est le moment de la séance.

> **Ce que je fais remarquer :** un écran utilisable au clavier, ce n'est
> pas une option pour les autres, c'est ce qui reste quand la souris tombe
> en panne — et notre jeu le casse tout seul, une fois par seconde, parce
> qu'il réécrit toute la page au lieu de changer ce qui a bougé.

**Pour avoir le temps** : mets `jour: 600` dans `regles/partie.yaml` avant
de lancer le serveur, sinon la phase change au milieu de ta démonstration.

**Ce qu'ils peuvent faire ensuite** (deux issues toutes prêtes) : ajouter un
style `:focus-visible` bien visible dans `site/css/site.css` ; ne réécrire
que ce qui a changé au lieu de toute la page dans `site/js/jeu.js`.

---

## Les trois réglages à poser avant chaque séance

Dans `regles/partie.yaml`, **avant** de lancer le serveur (le fichier n'est
lu qu'au démarrage) :

| Réglage | Valeur de démonstration | Pourquoi |
|---|---|---|
| `decouverte_du_role` | `300` en S2 | pour que l'écran du rôle reste affiché |
| `jour` | `600` en S4 | pour que la phase ne change pas au milieu |
| `delai_entre_les_arrivees` | `0.1` | pour que le village se remplisse tout de suite |

Et une fois la séance finie, remets les valeurs d'origine (10 secondes,
1.2 seconde) : ce sont celles du scénario de démonstration du README.

## Ce qui n'existe pas encore, dit clairement

1. **Il n'y a pas de fichier HTML par écran.** Le jeu est une seule page,
   `site/index.html`, remplie par `site/js/jeu.js` : il n'y a qu'une seule
   adresse, http://localhost:8000, et les écrans sont des moments de la
   partie, pas des pages. Pour en montrer un, il faut y jouer.
2. **L'écran de découverte du rôle n'est pas écrit en HTML sémantique.**
   Trois balises différentes, contre onze dans la carte des élèves.
3. **Aucun écran du jeu n'est parcourable au clavier plus d'une seconde**,
   et aucun style de focus n'est défini.

Ces trois points sont des tâches d'élèves, pas des accidents à cacher : ils
sont petits, visibles à l'écran, et vérifiables. C'est exactement ce qu'on
cherche pour une première contribution.
