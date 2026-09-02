# Le Bailli — Sombreval 1348

| | |
|---|---|
| **Univers** | Sombreval 1348 |
| **Camp** | Village |
| **Nombre par partie** | 1 |
| **Agit** | La nuit |
| **Statut** | Rôle de référence — les autres fiches suivent ce format |

Le bailli est l'officier du seigneur. Il rend la justice à Sombreval, il a le
droit d'entrer chez les gens et de leur poser des questions. Quand la peste
arrive et que le village accuse des « semeurs de peste » d'empoisonner les
puits, c'est lui qui enquête. La nuit, pendant que le village dort.

## Son pouvoir, en une phrase

> Chaque nuit, le bailli désigne un joueur vivant autre que lui, et le jeu lui
> répond « Semeur » ou « Villageois ».

Une phrase, un effet, une réponse. Si la fiche d'un rôle demande deux phrases,
c'est que le rôle fait deux choses : il faut le couper en deux ou le
simplifier.

## Quand il agit

- **Phase :** nuit.
- **Ordre :** après les Semeurs. Il apprend donc parfois qu'il a interrogé
  quelqu'un qui vient de mourir — le jeu le lui dit, ce n'est pas un bug.
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
6. La réponse dit le **camp**, pas le rôle : une guérisseuse et une paysanne
   renvoient toutes les deux « Villageois ».
7. Le jeu **garde la trace** de ce qu'il a appris et le lui réaffiche les
   nuits suivantes. Un joueur qui prend des notes sur une feuille ne doit pas
   être avantagé par rapport à un joueur qui n'en prend pas.

## Pourquoi c'est équilibré

Le bailli est la seule source d'information certaine du village. Sans lui, les
Semeurs gagnent presque toujours : le village vote au hasard le premier jour,
et un vote au hasard sur quinze joueurs ne trouve un Semeur qu'une fois sur
cinq.

Ce qui l'équilibre, c'est que **son information ne vaut rien tant qu'il ne
parle pas, et qu'elle le tue dès qu'il parle**. Le jour, s'il annonce « j'ai
interrogé Marion, c'est une Semeuse », il gagne un vote et signe sa mort la
nuit suivante : les Semeurs éliminent toujours le bailli connu en priorité.
Le vrai jeu du bailli n'est donc pas d'enquêter, c'est de choisir le moment où
il se déclare — ou de faire passer son information par quelqu'un d'autre.

Trois garde-fous supplémentaires :

- il n'apprend **qu'un joueur par nuit** : sur une partie de cinq nuits, il ne
  connaît au mieux que cinq joueurs sur quinze ;
- il apprend le **camp** et non le rôle, donc il ne peut pas repérer les
  autres pouvoirs du village et organiser le camp autour de lui ;
- rien ne prouve qu'il dit la vérité : **un Semeur peut prétendre être le
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
