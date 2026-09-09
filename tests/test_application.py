"""Le jeu complet, sans serveur : une horloge fausse et un joueur immobile.

L'horloge est fausse pour que la partie entière tienne en quelques
millisecondes au lieu de deux minutes.
"""

import random
import unittest

from jeu.application import Application
from jeu.configuration import Configuration
from jeu.erreurs import ErreurDeJeu


class HorlogeFausse(Application):
    """La même application, mais c'est le test qui décide de l'heure."""

    def __init__(self, graine=0):
        super().__init__(Configuration(), random.Random(graine))
        self.heure = 0.0

    def maintenant(self):
        return self.heure

    def avancer(self, secondes):
        self.heure += secondes


class TestApplication(unittest.TestCase):

    def setUp(self):
        self.jeu = HorlogeFausse()
        self.partie = self.jeu.creer_une_partie("Delphine", "sombreval")

    def _vue(self):
        return self.jeu.vue(self.partie["partie"], self.partie["jeton"])

    def _remplir_le_village(self):
        for _ in range(30):
            self.jeu.avancer(1.5)
            vue = self._vue()
            if len(vue["joueurs"]) == vue["joueurs_attendus"]:
                return vue
        self.fail("le village ne s'est jamais rempli")

    def _commencer(self):
        self._remplir_le_village()
        return self.jeu.commencer(self.partie["partie"], self.partie["jeton"])

    def test_ouvrir_une_partie_donne_un_lien_et_un_jeton(self):
        self.assertTrue(self.partie["partie"])
        self.assertTrue(self.partie["jeton"])

    def test_un_univers_pas_encore_ecrit_est_refuse(self):
        with self.assertRaises(ErreurDeJeu):
            self.jeu.creer_une_partie("Delphine", "salem")

    def test_les_joueurs_factices_arrivent_un_par_un(self):
        self.assertEqual(len(self._vue()["joueurs"]), 1)
        self.jeu.avancer(2)
        self.assertEqual(len(self._vue()["joueurs"]), 2)

    def test_le_village_se_remplit_puis_sarrete(self):
        vue = self._remplir_le_village()
        self.jeu.avancer(30)
        self.assertEqual(len(self._vue()["joueurs"]), vue["joueurs_attendus"])

    def test_on_ne_commence_pas_un_village_incomplet(self):
        with self.assertRaises(ErreurDeJeu):
            self.jeu.commencer(self.partie["partie"], self.partie["jeton"])

    def test_seul_le_createur_lance_la_partie(self):
        self._remplir_le_village()
        invite = self.jeu.parties[self.partie["partie"]].joueurs[1]
        with self.assertRaises(ErreurDeJeu):
            self.jeu.commencer(self.partie["partie"], invite.jeton)

    def test_un_jeton_inconnu_ne_donne_aucune_vue(self):
        with self.assertRaises(ErreurDeJeu):
            self.jeu.vue(self.partie["partie"], "jeton-invente")

    def test_une_partie_inconnue_est_refusee(self):
        with self.assertRaises(ErreurDeJeu):
            self.jeu.vue("partie-inventee", self.partie["jeton"])

    def test_la_partie_commence_par_la_decouverte_du_role(self):
        vue = self._commencer()
        self.assertEqual(vue["phase"], "decouverte")
        self.assertIsNotNone(vue["moi"]["role"])

    def test_les_phases_senchainent_toutes_seules(self):
        self._commencer()
        self.jeu.avancer(self.jeu.configuration.duree("decouverte_du_role") + 1)
        self.assertEqual(self._vue()["phase"], "nuit")
        self.jeu.avancer(self.jeu.configuration.duree("nuit") + 1)
        self.assertEqual(self._vue()["phase"], "jour")

    def test_on_ne_vote_pas_pendant_la_nuit(self):
        self._commencer()
        self.jeu.avancer(self.jeu.configuration.duree("decouverte_du_role") + 1)
        vue = self._vue()
        autre = next(j for j in vue["joueurs"] if j["numero"] != vue["moi"]["numero"])
        with self.assertRaises(ErreurDeJeu):
            self.jeu.agir(
                self.partie["partie"], self.partie["jeton"], "voter", autre["numero"]
            )

    def test_une_action_inconnue_est_refusee(self):
        self._commencer()
        with self.assertRaises(ErreurDeJeu):
            self.jeu.agir(self.partie["partie"], self.partie["jeton"], "danser", "j2")

    def test_une_partie_va_jusquau_bout_toute_seule(self):
        # Le joueur humain ne fait rien : les automates jouent, la partie
        # doit quand même se terminer et désigner un camp.
        self._commencer()
        for _ in range(300):
            self.jeu.avancer(2)
            vue = self._vue()
            if vue["phase"] == "fin":
                break
        self.assertEqual(vue["phase"], "fin")
        self.assertIn(vue["resultat"]["camp"], ("le Village", "les Loups"))
        self.assertEqual(len(vue["resultat"]["roles"]), 8)


if __name__ == "__main__":
    unittest.main()
