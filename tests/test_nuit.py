"""La résolution de la nuit : l'ordre des quatre étapes.

C'est le cœur du jeu, et l'endroit où une erreur ne se voit pas à l'œil nu :
d'où le nombre de tests.
"""

import unittest

from jeu.erreurs import ErreurDeJeu
from jeu.nuit import resoudre_la_nuit
from jeu.pouvoirs import choisir_une_cible, cibles_possibles
from tests.fabrique import partie_pour_les_tests

# Deux loups, un bailli, un chevalier, une herboriste, trois manants :
# la composition à huit joueurs de la démonstration.
COMPOSITION = [
    "menace", "menace", "enqueteur", "protecteur",
    "guerisseur", "villageois", "villageois", "villageois",
]


class TestNuit(unittest.TestCase):

    def setUp(self):
        self.partie = partie_pour_les_tests(COMPOSITION)
        self.loup, self.autre_loup = self.partie.joueurs[0], self.partie.joueurs[1]
        self.bailli = self.partie.joueurs[2]
        self.chevalier = self.partie.joueurs[3]
        self.herboriste = self.partie.joueurs[4]
        self.manant = self.partie.joueurs[5]

    def test_la_menace_elimine_sa_victime(self):
        self._viser(self.loup, self.manant)
        self._viser(self.autre_loup, self.manant)
        resoudre_la_nuit(self.partie)
        self.assertFalse(self.manant.vivant)

    def test_une_victime_protegee_survit(self):
        self._viser(self.loup, self.manant)
        self._viser(self.autre_loup, self.manant)
        self._viser(self.chevalier, self.manant)
        resoudre_la_nuit(self.partie)
        self.assertTrue(self.manant.vivant)

    def test_le_journal_dit_le_role_du_mort(self):
        self._viser(self.loup, self.bailli)
        self._viser(self.autre_loup, self.bailli)
        resoudre_la_nuit(self.partie)
        dernier = self.partie.journal[-1]["texte"]
        self.assertIn(self.bailli.pseudo, dernier)
        self.assertIn("le Bailli", dernier)

    def test_le_vote_interne_de_la_menace_suit_la_majorite(self):
        # Trois loups pour avoir une vraie majorité : deux voix contre une.
        partie = partie_pour_les_tests(["menace"] * 3 + ["villageois"] * 4)
        loups = partie.joueurs[:3]
        vise, epargne = partie.joueurs[3], partie.joueurs[4]
        choisir_une_cible(partie, loups[0], vise.numero)
        choisir_une_cible(partie, loups[1], vise.numero)
        choisir_une_cible(partie, loups[2], epargne.numero)

        resoudre_la_nuit(partie)

        self.assertFalse(vise.vivant)
        self.assertTrue(epargne.vivant)

    def test_une_egalite_dans_la_menace_est_tranchee_au_hasard(self):
        premier, second = self.partie.joueurs[5], self.partie.joueurs[6]
        self._viser(self.loup, premier)
        self._viser(self.autre_loup, second)

        resoudre_la_nuit(self.partie)

        morts = [j for j in (premier, second) if not j.vivant]
        self.assertEqual(len(morts), 1)

    def test_celui_qui_ne_joue_pas_ne_fait_rien(self):
        # Personne n'a choisi : le jeu ne choisit pas à leur place.
        resoudre_la_nuit(self.partie)
        self.assertEqual(len(self.partie.vivants()), 8)

    def test_le_bailli_apprend_le_camp_de_sa_cible(self):
        self._viser(self.bailli, self.loup)
        resoudre_la_nuit(self.partie)
        self.assertIn("un loup", self._dernier_secret(self.bailli))

    def test_le_bailli_ne_lit_que_letat_du_debut_de_nuit(self):
        # Le bailli sonde le manant ; les loups le tuent la même nuit.
        # Il doit apprendre son camp, et rien de plus : sa révélation ne
        # dit pas qu'il est mort — le village l'apprendra au matin.
        self._viser(self.bailli, self.manant)
        self._viser(self.loup, self.manant)
        self._viser(self.autre_loup, self.manant)

        resoudre_la_nuit(self.partie)

        self.assertFalse(self.manant.vivant)
        self.assertIn("quelqu'un du village", self._dernier_secret(self.bailli))

    def test_le_bailli_tue_cette_nuit_apprend_quand_meme(self):
        self._viser(self.bailli, self.manant)
        self._viser(self.loup, self.bailli)
        self._viser(self.autre_loup, self.bailli)

        resoudre_la_nuit(self.partie)

        self.assertFalse(self.bailli.vivant)
        self.assertIn("quelqu'un du village", self._dernier_secret(self.bailli))

    def test_le_bailli_ne_peut_pas_sonder_deux_fois_de_suite_le_meme(self):
        self._viser(self.bailli, self.manant)
        resoudre_la_nuit(self.partie)

        permises = cibles_possibles(self.partie, self.bailli)
        self.assertNotIn(self.manant, permises)

    def test_le_chevalier_peut_reproteger_apres_une_nuit_de_pause(self):
        self._viser(self.chevalier, self.manant)
        resoudre_la_nuit(self.partie)
        self._viser(self.chevalier, self.bailli)
        resoudre_la_nuit(self.partie)

        self.assertIn(self.manant, cibles_possibles(self.partie, self.chevalier))

    def test_lherboriste_ne_soigne_quune_fois(self):
        self._viser(self.herboriste, self.herboriste)  # elle peut se soigner
        resoudre_la_nuit(self.partie)

        self.assertEqual(cibles_possibles(self.partie, self.herboriste), [])

    def test_un_loup_ne_vise_pas_un_loup(self):
        permises = cibles_possibles(self.partie, self.loup)
        self.assertNotIn(self.autre_loup, permises)

    def test_viser_une_cible_interdite_est_refuse(self):
        with self.assertRaises(ErreurDeJeu):
            choisir_une_cible(self.partie, self.loup, self.autre_loup.numero)

    def test_un_manant_na_rien_a_faire_la_nuit(self):
        self.assertEqual(cibles_possibles(self.partie, self.manant), [])

    def test_un_mort_ne_joue_plus(self):
        self.manant.vivant = False
        with self.assertRaises(ErreurDeJeu):
            choisir_une_cible(self.partie, self.manant, self.loup.numero)

    # --- petites aides -----------------------------------------------------

    def _viser(self, joueur, cible):
        choisir_une_cible(self.partie, joueur, cible.numero)

    def _dernier_secret(self, joueur):
        return self.partie.revelations[joueur.numero][-1]["texte"]


if __name__ == "__main__":
    unittest.main()
