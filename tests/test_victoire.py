"""Les deux conditions de victoire, et rien d'autre."""

import unittest

from jeu.victoire import camp_gagnant
from tests.fabrique import partie_pour_les_tests


class TestVictoire(unittest.TestCase):

    def test_la_partie_continue_tant_que_le_village_est_le_plus_nombreux(self):
        partie = partie_pour_les_tests(["menace", "villageois", "villageois"])
        self.assertIsNone(camp_gagnant(partie))

    def test_le_village_gagne_quand_la_menace_est_eliminee(self):
        partie = partie_pour_les_tests(["menace", "villageois", "villageois"])
        partie.joueurs[0].vivant = False
        self.assertEqual(camp_gagnant(partie), "village")

    def test_la_menace_gagne_quand_elle_egale_les_autres(self):
        partie = partie_pour_les_tests(["menace", "villageois", "villageois"])
        partie.joueurs[1].vivant = False
        self.assertEqual(camp_gagnant(partie), "menace")

    def test_la_menace_gagne_quand_elle_depasse_les_autres(self):
        partie = partie_pour_les_tests(["menace", "menace", "villageois"])
        self.assertEqual(camp_gagnant(partie), "menace")


if __name__ == "__main__":
    unittest.main()
