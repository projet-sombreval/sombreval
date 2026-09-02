"""Tests des univers.

Lancement, depuis la racine du dépôt :

    python3 -m unittest discover tests
"""

import unittest

from jeu.univers import UNIVERS, chercher_univers, noms_univers


class TestUnivers(unittest.TestCase):

    def test_il_y_a_trois_univers(self):
        self.assertEqual(len(UNIVERS), 3)

    def test_les_trois_univers_sont_ceux_annonces(self):
        self.assertEqual(
            noms_univers(), ["sombreval", "salem", "serenissime"]
        )

    def test_chercher_un_univers_connu(self):
        univers = chercher_univers("salem")
        self.assertEqual(univers["annee"], 1692)

    def test_chercher_un_univers_inconnu_leve_une_erreur(self):
        with self.assertRaises(ValueError):
            chercher_univers("atlantide")

    def test_chaque_univers_a_les_memes_informations(self):
        attendus = {
            "titre", "annee", "sous_titre", "camp_village", "camp_traitre"
        }
        for nom, univers in UNIVERS.items():
            with self.subTest(univers=nom):
                self.assertEqual(set(univers), attendus)


if __name__ == "__main__":
    unittest.main()
