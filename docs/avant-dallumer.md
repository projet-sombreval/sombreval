# Avant d'allumer un monde

<!-- ── À TOI · GARDIENNE DU DÉPÔT ──────────────────────
Le fichier porte cinq conditions à remplir avant qu'un
monde puisse être allumé. Leur colonne de droite est
vide : c'est elle que tu écris, et elle demande comment
on vérifie chacune.

Une phrase par condition, et elle doit dire le geste :
« on ouvre le fichier et on compte les sept couleurs »
se fait ; « on s'assure que c'est complet » ne se fait
pas.

Et ce soir, c'est toi qui dis si on allume. Avant chaque
intégration, tu passes ta liste sur le monde concerné et
tu annonces à voix haute : complet, ou bien ce qui
manque.
────────────────────────────────────────────────────── -->

Un univers passe à `disponible: true` quand les cinq lignes suivantes sont
vraies. Elles se vérifient, elles ne se discutent pas.

| | Ce qu'on vérifie | Comment |
|---|---|---|
| 1 | les sept couleurs sont présentes, et ce sont les sept noms imposés | |
| 2 | aucune des sept n'est illisible sur les autres | |
| 3 | la présentation est écrite | |
| 4 | le titre, l'année et le sous-titre sont là | |
| 5 | le monde apparaît sur `/api/univers` après redéploiement | |

Le geste d'allumer appartient à l'ambassadrice du monde, et à elle seule :
c'est une ligne dans son propre fichier.
