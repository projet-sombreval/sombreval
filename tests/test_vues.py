"""L'autorité du serveur : ce qui n'est pas affiché n'est pas dans la page.

Ces tests-là ne vérifient pas ce que le joueur voit, mais ce qu'il ne
reçoit PAS. On fabrique sa vue, on la met à plat, et on cherche dedans ce
qui ne devrait pas y être — exactement ce que ferait un élève curieux avec
l'inspecteur de son navigateur.
"""

import json
import unittest

from jeu.pouvoirs import choisir_une_cible
from jeu.vues import vue_pour
from tests.fabrique import partie_pour_les_tests

COMPOSITION = [
    "menace", "menace", "enqueteur", "protecteur",
    "guerisseur", "villageois", "villageois", "villageois",
]


class TestVueFiltree(unittest.TestCase):

    def setUp(self):
        self.partie = partie_pour_les_tests(COMPOSITION)
        self.loup, self.autre_loup = self.partie.joueurs[0], self.partie.joueurs[1]
        self.bailli = self.partie.joueurs[2]
        self.manant = self.partie.joueurs[5]

    def _vue(self, joueur):
        return vue_pour(self.partie, joueur, maintenant=0.0)

    def _a_plat(self, joueur):
        return json.dumps(self._vue(joueur), ensure_ascii=False)

    def test_je_vois_mon_role(self):
        self.assertEqual(self._vue(self.bailli)["moi"]["role"]["nom"], "le Bailli")

    def test_je_ne_vois_le_role_daucun_autre_vivant(self):
        vue = self._vue(self.manant)
        autres = [j for j in vue["joueurs"] if j["numero"] != self.manant.numero]
        for joueur in autres:
            with self.subTest(joueur=joueur["pseudo"]):
                self.assertNotIn("role", joueur)

    def test_le_nom_des_autres_roles_nest_meme_pas_dans_la_page(self):
        # Personne n'est mort : aucun nom de rôle n'a de raison d'apparaître,
        # sauf le mien.
        page = self._a_plat(self.manant)
        for nom in ("le Loup", "le Bailli", "le Chevalier", "l'Herboriste"):
            with self.subTest(role=nom):
                self.assertNotIn(nom, page)

    def test_aucun_jeton_secret_ne_sort_du_serveur(self):
        page = self._a_plat(self.manant)
        for joueur in self.partie.joueurs:
            with self.subTest(joueur=joueur.pseudo):
                self.assertNotIn(joueur.jeton, page)

    def test_les_loups_se_connaissent(self):
        vue = self._vue(self.loup)
        complice = self._joueur_vu(vue, self.autre_loup)
        self.assertEqual(complice["role"], "le Loup")

    def test_un_villageois_ne_voit_pas_le_vote_des_loups(self):
        choisir_une_cible(self.partie, self.loup, self.manant.numero)
        self.assertEqual(self._vue(self.manant).get("choix_des_allies", []), [])

    def test_un_loup_voit_le_choix_de_son_complice(self):
        choisir_une_cible(self.partie, self.loup, self.manant.numero)
        choix = self._vue(self.autre_loup)["choix_des_allies"]
        self.assertIn(
            {"pseudo": self.loup.pseudo, "cible": self.manant.pseudo}, choix
        )

    def test_le_role_dun_mort_est_revele_a_tous(self):
        self.bailli.vivant = False
        vue = self._vue(self.manant)
        self.assertEqual(self._joueur_vu(vue, self.bailli)["role"], "le Bailli")

    def test_a_la_fin_tout_le_monde_voit_tout(self):
        self.partie.phase = "fin"
        self.partie.camp_gagnant = "village"
        vue = self._vue(self.manant)
        self.assertEqual(len(vue["resultat"]["roles"]), 8)
        for joueur in vue["joueurs"]:
            with self.subTest(joueur=joueur["pseudo"]):
                self.assertIn("role", joueur)

    def test_je_ne_recois_que_mes_propres_secrets(self):
        self.partie.noter_pour(self.bailli, "un secret de bailli")
        self.assertEqual(self._vue(self.manant)["mes_revelations"], [])
        self.assertEqual(len(self._vue(self.bailli)["mes_revelations"]), 1)

    def test_le_manant_na_aucune_cible_la_nuit(self):
        self.assertEqual(self._vue(self.manant)["cibles"], [])

    def _joueur_vu(self, vue, joueur):
        return next(j for j in vue["joueurs"] if j["numero"] == joueur.numero)


if __name__ == "__main__":
    unittest.main()
