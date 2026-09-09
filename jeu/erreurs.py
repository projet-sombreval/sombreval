"""L'erreur unique du jeu.

Toutes les erreurs prévisibles (pseudo déjà pris, partie pleine, ce n'est pas
à toi de jouer…) sont des ErreurDeJeu. Leur message est écrit pour être
affiché tel quel au joueur : pas de jargon, pas de nom de fonction.
"""


class ErreurDeJeu(Exception):
    pass
