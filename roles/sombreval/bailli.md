# Le Bailli — Sombreval 1348

| | |
|---|---|
| **Univers** | Sombreval 1348 |
| **Camp** | Village |
| **Nom dans le moteur** | `enqueteur` (voir `regles/roles.yaml`) |
| **Nombre par partie** | 1 |
| **Agit** | La nuit |
| **Statut** | Rôle de référence — les autres fiches suivent ce format |

Le bailli est l'officier du seigneur. Il rend la justice à Sombreval, il a le
droit d'entrer chez les gens et de leur poser des questions. Quand la peste
arrive et que le village se met à chercher des coupables, c'est lui qui
enquête. La nuit, pendant que le village dort.

## Son pouvoir, en une phrase

> Chaque nuit, le bailli désigne un joueur vivant autre que lui, et le jeu lui
> répond « un loup » ou « quelqu'un du village ».

Une phrase, un effet, une réponse. Si la fiche d'un rôle demande deux phrases,
c'est que le rôle fait deux choses : il faut le couper en deux ou le
simplifier.

## Quand il agit

- **Phase :** nuit.
- **Ordre :** tout le monde joue en même temps ; il n'y a pas d'ordre de
  réveil. C'est le serveur qui résout la nuit, sur l'état du village figé au
  début de la nuit. Le bailli apprend donc parfois le camp de quelqu'un qui
  vient de mourir — ce n'est pas un bug, c'est cet ordre-là.
- **Fréquence :** une fois par nuit, obligatoire. S'il ne choisit personne
  avant la fin du temps imparti, le jeu ne choisit pas à sa place : il perd
  simplement son tour.
- **Il s'arrête de jouer** dès qu'il est mort. Son rôle est alors révélé à
  tous, comme celui de n'importe quel mort.

## Ce que le jeu doit vérifier

Ce sont les règles que le code doit faire respecter. Chacune mérite un test.

1. La cible est un joueur **vivant**.
2. La cible **n'est pas le bailli lui-même**.
3. Le bailli est **vivant** au moment où il agit.
4. Il n'a **pas déjà interrogé** cette nuit.
5. La réponse est envoyée **au bailli seul** : elle n'apparaît ni dans le
   journal public, ni sur l'écran d'un autre joueur, ni dans le récit du
   matin.
6. La réponse dit le **camp**, pas le rôle : l'Herboriste et le Manant
   renvoient tous les deux « quelqu'un du village ».
7. Le jeu **garde la trace** de ce qu'il a appris et le lui réaffiche les
   nuits suivantes. Un joueur qui prend des notes sur une feuille ne doit pas
   être avantagé par rapport à un joueur qui n'en prend pas.

## Pourquoi c'est équilibré

Le bailli est la seule source d'information certaine du village. Sans lui, les
loups gagnent presque toujours : le village vote au hasard le premier jour,
et un vote au hasard sur huit joueurs ne trouve un loup qu'une fois sur
quatre.

Ce qui l'équilibre, c'est que **son information ne vaut rien tant qu'il ne
parle pas, et qu'elle le tue dès qu'il parle**. Le jour, s'il annonce « j'ai
sondé Marion, c'est une louve », il gagne un vote et signe sa mort la
nuit suivante : les loups éliminent toujours le bailli connu en priorité.
Le vrai jeu du bailli n'est donc pas d'enquêter, c'est de choisir le moment où
il se déclare — ou de faire passer son information par quelqu'un d'autre.

Trois garde-fous supplémentaires :

- il n'apprend **qu'un joueur par nuit**, et jamais le même deux nuits de
  suite : sur une partie de trois nuits, il ne connaît au mieux que trois
  joueurs sur huit ;
- il apprend le **camp** et non le rôle, donc il ne peut pas repérer les
  autres pouvoirs du village et organiser le camp autour de lui ;
- rien ne prouve qu'il dit la vérité : **un loup peut prétendre être le
  bailli**, et c'est même la meilleure façon pour lui de gagner la journée. Le
  village doit arbitrer entre deux baillis qui s'accusent, ce qui est
  exactement la situation intéressante.

## Ce qui n'a pas été retenu

- **Deux baillis dans les grandes parties.** Deux sources d'information sûres
  qui se confirment l'une l'autre rendent le mensonge impossible à tenir.
- **Le bailli apprend le rôle exact.** Trop fort : il repère les pouvoirs du
  village dès la deuxième nuit et le camp s'organise autour de lui.
- **Le bailli survit à la première attaque.** Un rôle qui cumule information
  et protection n'a plus de risque à prendre, et le dilemme décrit plus haut
  disparaît.
