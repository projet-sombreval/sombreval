# Quand est-ce qu'un écran est fini ?

Cette liste est écrite par l'équipe technique. Elle vaut pour nos écrans, et
pour ceux que l'atelier design nous livre — D3 la salle d'attente, D4 la
carte de rôle, D5 l'écran de jour, D6 l'écran de nuit, D7 l'écran final.

**Un critère n'est pas un avis.** Il se contrôle en un geste, et deux
personnes qui le contrôlent trouvent la même chose. Un écran qui n'en respecte
pas un n'est pas fini : il est renvoyé, avec le numéro du critère.

| | Le critère | Comment on le contrôle |
|---|---|---|
| 1 | Les couleurs portent les mêmes noms de variables que les autres écrans | on cherche les lignes qui commencent par deux tirets, et on vérifie qu'on lit les sept mêmes noms |
| 2 | Une seule police, et trois tailles de texte au maximum | on compte les polices et les tailles déclarées |
| 3 | Tous les espacements sont pris dans l'échelle 4 · 8 · 16 · 24 · 32 | on relève chaque `margin` et chaque `padding`, et on cherche l'intruse |
| 4 | Un seul modèle de bouton, partout | on les met côte à côte, et on compare hauteur, bordure et survol |
| 5 | Chaque champ de saisie a une étiquette visible, pas seulement un texte d'exemple | on tape dans le champ : l'étiquette doit rester à l'écran |
| 6 | On voit où on est quand on navigue à la touche Tab | on appuie plusieurs fois sur Tab, sans toucher la souris |
| 7 | Rien ne déborde sur un écran large de 360 pixels | on réduit la fenêtre à 360 px dans les outils du navigateur |
| 8 | Les états — désactivé, erreur, chargement — ne se reconnaissent pas à la couleur seule | on regarde l'écran en noir et blanc : l'état doit encore se voir |

Le critère 8 ne s'appliquait pas à nos deux premiers écrans, qui n'avaient pas
d'états. Il s'applique à partir de la salle d'attente, où un joueur est « en
attente » ou « prêt ».

*Écrite le 2 novembre 2026 par l'équipe technique, à partir de la comparaison
de ses deux premiers écrans.*
