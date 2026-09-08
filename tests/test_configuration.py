"""Les fichiers de regles/ sont lus, et ce qu'ils contiennent tient debout."""

import unittest

from jeu.configuration import Configuration
from jeu.erreurs import ErreurDeJeu

ROLES_ATTENDUS = {
    "menace", "espion", "traitre", "enqueteur", "temoin",
    "protecteur", "guerisseur", "justicier", "doyen", "villageois",
}


class TestConfiguration(unittest.TestCase):

    def setUp(self):
        self.configuration = Configuration()

    def test_les_dix_roles_sont_decrits(self):
        self.assertEqual(set(self.configuration.roles), ROLES_ATTENDUS)

    def test_chaque_role_a_un_camp_et_une_action(self):
        for nom, regle in self.configuration.roles.items():
            with self.subTest(role=nom):
                self.assertIn(regle["camp"], ("village", "menace"))
                self.assertIn("action", regle)

    def test_les_trois_univers_sont_lus(self):
        self.assertEqual(
            set(self.configuration.univers), {"sombreval", "salem", "serenissime"}
        )

    def test_sombreval_nomme_les_dix_roles(self):
        univers = self.configuration.univers_choisi("sombreval")
        self.assertEqual(set(univers["roles"]), ROLES_ATTENDUS)

    def test_un_univers_pas_encore_ecrit_est_refuse(self):
        with self.assertRaises(ErreurDeJeu):
            self.configuration.univers_choisi("salem")

    def test_la_composition_a_huit_fait_bien_huit_joueurs(self):
        composition = self.configuration.composition(8)
        self.assertEqual(sum(composition.values()), 8)

    def test_une_composition_avec_un_role_pas_encore_joue_est_refusee(self):
        # Le Doyen est décrit dans regles/roles.yaml mais « implemente:
        # false » : le moteur doit refuser de lancer la partie plutôt que de
        # se bloquer en pleine séance.
        self.configuration.compositions[3] = {"menace": 1, "doyen": 2}
        with self.assertRaises(ErreurDeJeu):
            self.configuration.composition(3)

    def test_les_durees_sont_courtes_pour_la_demonstration(self):
        for phase in ("nuit", "jour"):
            self.assertLessEqual(self.configuration.duree(phase), 60)


if __name__ == "__main__":
    unittest.main()
