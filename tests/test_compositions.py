"""La table des compositions : aucun effectif oublié."""

# ── À TOI · GARDIENNE DU DÉPÔT ──────────────────────
# Un test qui parcourt la table et vérifie qu'aucun
# effectif n'est oublié, de six à douze. C'est le genre
# d'oubli qu'on ne voit qu'en jouant.
#
# Où trouver les données : la table est
# Configuration().compositions, un dictionnaire — pour
# chaque nombre de joueurs, sa composition
# (Configuration se trouve dans jeu.configuration).
#
# En attendant, le test ci-dessous passe et ne vérifie
# rien : c'est ce qui garde la vérification verte. Tu
# remplaces tout son contenu.
# ──────────────────────────────────────────────────────

import unittest


class TestCompositions(unittest.TestCase):

    def test_a_toi(self):
        pass


if __name__ == "__main__":
    unittest.main()
