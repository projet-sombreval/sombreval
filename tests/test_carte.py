"""Ce que la carte d'une joueuse peut savoir, dans les trois mondes."""

# ── À TOI · GARDIENNE DU DÉPÔT ──────────────────────
# Un test qui vérifie, dans les trois mondes, que le
# serveur n'envoie le rôle d'une autre joueuse que dans
# les quatre cas. C'est la leçon de la séance, écrite en
# code : si quelqu'un desserre la règle un jour, c'est ton
# test qui tombera.
#
# Où trouver les données : ce que le serveur envoie à une
# joueuse, c'est sa vue — Application().vue(partie,
# jeton)["joueurs"]. tests/test_vues.py en montre un
# exemple (Application se trouve dans jeu.application).
#
# En attendant, le test ci-dessous passe et ne vérifie
# rien : c'est ce qui garde la vérification verte. Tu
# remplaces tout son contenu.
# ──────────────────────────────────────────────────────

import unittest


class TestCarte(unittest.TestCase):

    def test_a_toi(self):
        pass


if __name__ == "__main__":
    unittest.main()
