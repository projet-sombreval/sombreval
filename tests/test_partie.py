"""La salle d'attente et le tirage des rôles."""

import unittest

from jeu.erreurs import ErreurDeJeu
from jeu.partie import ajouter_un_joueur, distribuer_les_roles
from tests.fabrique import CONFIGURATION, partie_pour_les_tests


class TestSalleDAttente(unittest.TestCase):

    def setUp(self):
        self.partie = partie_pour_les_tests([], phase="attente")

    def test_le_premier_arrive_est_le_createur(self):
        joueur = ajouter_un_joueur(self.partie, "Delphine")
        self.assertEqual(self.partie.createur, joueur.numero)

    def test_un_pseudonyme_vide_est_refuse(self):
        with self.assertRaises(ErreurDeJeu):
            ajouter_un_joueur(self.partie, "   ")

    def test_un_pseudonyme_trop_long_est_refuse(self):
        with self.assertRaises(ErreurDeJeu):
            ajouter_un_joueur(self.partie, "a" * 21)

    def test_un_pseudonyme_deja_pris_est_refuse(self):
        ajouter_un_joueur(self.partie, "Delphine")
        with self.assertRaises(ErreurDeJeu):
            ajouter_un_joueur(self.partie, "delphine")

    def test_le_neuvieme_joueur_est_refuse(self):
        for numero in range(8):
            ajouter_un_joueur(self.partie, f"Joueur{numero}")
        with self.assertRaises(ErreurDeJeu):
            ajouter_un_joueur(self.partie, "DeTrop")

    def test_on_ne_rejoint_pas_une_partie_commencee(self):
        self.partie.phase = "nuit"
        with self.assertRaises(ErreurDeJeu):
            ajouter_un_joueur(self.partie, "EnRetard")

    def test_chaque_joueur_a_deux_identites(self):
        premier = ajouter_un_joueur(self.partie, "Delphine")
        second = ajouter_un_joueur(self.partie, "Perrine")
        self.assertNotEqual(premier.numero, second.numero)
        self.assertNotEqual(premier.jeton, second.jeton)


class TestDistributionDesRoles(unittest.TestCase):

    def setUp(self):
        self.partie = partie_pour_les_tests([], phase="attente")
        for numero in range(8):
            ajouter_un_joueur(self.partie, f"Joueur{numero}")
        # Les tests ne dépendent pas du réglage de démonstration.
        self.role_impose = CONFIGURATION.parametres["role_du_createur"]
        CONFIGURATION.parametres["role_du_createur"] = None

    def tearDown(self):
        CONFIGURATION.parametres["role_du_createur"] = self.role_impose

    def test_tout_le_monde_recoit_un_role(self):
        distribuer_les_roles(self.partie)
        for joueur in self.partie.joueurs:
            with self.subTest(joueur=joueur.pseudo):
                self.assertIsNotNone(joueur.role)

    def test_la_composition_est_respectee(self):
        distribuer_les_roles(self.partie)
        compte = {}
        for joueur in self.partie.joueurs:
            compte[joueur.role] = compte.get(joueur.role, 0) + 1
        self.assertEqual(compte, CONFIGURATION.composition(8))

    def test_le_role_du_createur_peut_etre_impose_pour_repeter(self):
        CONFIGURATION.parametres["role_du_createur"] = "enqueteur"
        distribuer_les_roles(self.partie)
        createur = self.partie.joueur_par_numero(self.partie.createur)
        self.assertEqual(createur.role, "enqueteur")

    def test_un_role_impose_hors_composition_est_refuse(self):
        CONFIGURATION.parametres["role_du_createur"] = "doyen"
        with self.assertRaises(ErreurDeJeu):
            distribuer_les_roles(self.partie)


if __name__ == "__main__":
    unittest.main()
