# Contribuer au projet Sombreval

Trois règles. Elles tiennent sur cette page, et elles ne changent pas.

## 1. Une tâche = une branche = une pull request relue

Une **tâche** est une chose à faire, décrite dans une *issue* : « ajouter la
carte de la guérisseuse », « corriger le compte des votes en cas d'égalité ».
Une tâche, pas trois.

Une **branche** est une copie de travail du projet, où tu modifies ce que tu
veux sans gêner personne.

Une **pull request** (PR) est la demande d'ajouter ton travail au projet. Elle
est **relue par quelqu'un d'autre** avant d'être acceptée. Une PR que
personne n'a relue n'entre pas dans le projet, même si elle est parfaite.

```bash
git checkout main                       # se placer sur la branche principale
git pull                                # récupérer le travail des autres
git checkout -b carte-guerisseuse       # créer sa branche et s'y placer
# ... tu travailles, tu enregistres ...
git add cartes/marion-guerisseuse.html cartes/marion-guerisseuse.css
git commit -m "Ajouter la carte de la guérisseuse"
git push -u origin carte-guerisseuse    # envoyer sa branche sur GitHub
```

Ensuite, sur GitHub : bouton **Compare & pull request**, tu remplis le
formulaire qui s'affiche, tu envoies. Le formulaire pose trois questions ;
réponds-y en français, en une phrase chacune.

Nomme ta branche d'après ce qu'elle fait : `carte-guerisseuse`,
`corriger-egalite-votes`. Que des minuscules, des tirets, pas d'accent.

## 2. Écrire un message de commit

Un **commit** est un point de sauvegarde. Son message dit ce que tu as fait,
pour que celui qui lira l'historique dans six mois comprenne sans ouvrir le
code.

La règle : **un verbe à l'infinitif, ce que ça fait, en moins de 60
caractères.**

| Bon | Mauvais | Pourquoi |
|---|---|---|
| `Ajouter la carte de la guérisseuse` | `carte` | On ne sait pas ce qui a été fait. |
| `Corriger le vote en cas d'égalité` | `fix bug` | En français, et on dit lequel. |
| `Renommer bailli.md en minuscules` | `modifs` | « modifs » ne veut rien dire. |
| `Écrire le test de fin de partie` | `ça marche enfin !!!` | L'historique n'est pas un journal intime. |

Si tu as besoin d'expliquer **pourquoi**, saute une ligne et écris un
paragraphe en dessous. Le *quoi* se lit dans le code ; le *pourquoi*, non.

Un commit = une idée. Si ton message contient « et », tu as sans doute deux
commits à faire.

## 3. Jamais rien directement sur `main`

`main` est la branche du jeu qui marche. C'est celle qu'on lancera devant la
classe en mai.

Personne n'y écrit directement. Jamais. Pas même pour une virgule, pas même le
professeur. Tout y entre par une pull request relue.

Si tu t'aperçois que tu as travaillé sur `main` par erreur, ne pousse rien et
demande : ça se rattrape en deux commandes, tant que rien n'est envoyé.

## Avant d'ouvrir ta pull request

- [ ] les tests passent : `python3 -m unittest discover tests` ;
- [ ] si tu as touché à une page ou à une carte, tu l'as ouverte dans le
      navigateur et regardée ;
- [ ] tu n'as modifié que les fichiers de ta tâche — `git status` te dit
      lesquels tu as touchés ;
- [ ] ton nom de branche et tes messages de commit suivent les règles
      ci-dessus.

## En cas de doute

Ouvre une issue avec le gabarit **Bug** ou **Nouvelle fonctionnalité**, ou
pose la question dans ta pull request. Une question posée coûte cinq minutes ;
un fichier écrasé, une séance.
