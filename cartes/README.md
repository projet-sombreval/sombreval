# cartes/ — le dossier des élèves

C'est ici que chacun dépose la carte de personnage qu'il a fabriquée en
séances 2 à 4. En séance 5, ce dossier doit contenir une carte par élève.

Une carte de personnage, c'est ce qu'un joueur a sous les yeux pendant la
partie : le nom de son rôle, son pouvoir, son camp. Une page, pas plus.

## Ce que tu déposes

Deux fichiers, et deux seulement :

- `<pseudo>-<role>.html` — le contenu de la carte ;
- `<pseudo>-<role>.css` — son apparence.

Exemples de noms corrects :

```
marion-guerisseuse.html    marion-guerisseuse.css
tarek-inquisiteur.html     tarek-inquisiteur.css
lou-doge.html              lou-doge.css
```

Règles de nommage — elles évitent que deux personnes écrasent le travail de
l'autre :

- que des minuscules ;
- pas d'accent, pas d'espace, pas de caractère spécial : `guerisseuse` et non
  `Guérisseuse` ni `guérisseuse` ;
- un tiret entre le pseudo et le rôle, et un seul ;
- le même nom pour le `.html` et le `.css` ;
- ton pseudo est celui que tu utilises dans le jeu, pas ton prénom d'état
  civil.

## Comment commencer

1. Ouvre `exemple-bailli.html` dans ton navigateur : tu vois la carte finie.
2. Ouvre les deux fichiers d'exemple dans ton éditeur et lis les commentaires.
3. Copie-les sous ton nom à toi :

   ```bash
   cp cartes/exemple-bailli.html cartes/marion-guerisseuse.html
   cp cartes/exemple-bailli.css cartes/marion-guerisseuse.css
   ```

4. Dans ton `.html`, change la ligne `<link rel="stylesheet" ...>` pour
   qu'elle pointe vers **ton** `.css`. Si tu oublies, ta carte s'affiche en
   noir et blanc : c'est le signe.
5. Change le contenu, puis les couleurs.
6. Ouvre ton fichier dans le navigateur après **chaque** modification.

Le pouvoir écrit sur ta carte doit être celui de la fiche technique du rôle,
dans `roles/`. Si les deux ne disent pas la même chose, c'est la fiche de
`roles/` qui a raison.

## C'est fini quand

- [ ] mes deux fichiers sont nommés comme il faut ;
- [ ] la carte s'ouvre dans le navigateur sans erreur ;
- [ ] le nom du rôle, le pouvoir, le camp et le moment où il agit sont tous
      lisibles sur la carte ;
- [ ] le pouvoir tient en une phrase ;
- [ ] sur un téléphone, aucun texte ne dépasse de l'écran et il n'y a rien à
      faire défiler sur le côté ;
- [ ] mon CSS ne touche qu'à ma carte : je n'ai pas modifié
      `exemple-bailli.css` ni le fichier de quelqu'un d'autre ;
- [ ] mes couleurs sont dans les variables du haut du fichier, pas éparpillées
      dans tout le CSS.

## Vérifier la lisibilité sur téléphone

Sans téléphone sous la main : dans Firefox ou Chrome, appuie sur `F12`, puis
sur l'icône en forme de téléphone en haut de la fenêtre qui s'ouvre. Choisis
une largeur de 360 pixels. Tout doit rester lisible.

## Pour déposer ta carte

Une carte = une branche = une pull request, comme tout le reste du projet.
La marche à suivre est dans [CONTRIBUTING.md](../CONTRIBUTING.md).

Ne touche jamais aux fichiers `exemple-bailli.*` : ils servent de modèle à
toute la classe.
