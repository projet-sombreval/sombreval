"""Une partie a la taille qu'on lui choisit, et annonce sa composition.

Le nombre de joueurs n'est plus un réglage unique du jeu : chaque partie le
choisit à sa création, parmi les tailles que regles/roles.yaml sait composer.
Et la composition est annoncée à tous — combien de chaque rôle, jamais qui
les porte.

La table réelle ne connaît que huit joueurs : ces tests en ajoutent une
seconde, à six, dans une copie des règles.
"""

import itertools
import random
import shutil
import tempfile
import unittest
from pathlib import Path

import yaml

from jeu.application import Application
from jeu.configuration import DOSSIER_REGLES, Configuration
from jeu.erreurs import ErreurDeJeu

SIX = {"menace": 1, "enqueteur": 1, "protecteur": 1, "villageois": 3}


class TestLaTailleDUnePartie(unittest.TestCase):

    def setUp(self):
        self.dossier = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.dossier)
        shutil.copytree(DOSSIER_REGLES, self.dossier, dirs_exist_ok=True)
        roles = yaml.safe_load((self.dossier / "roles.yaml").read_text(encoding="utf-8"))
        roles["compositions"][6] = SIX
        (self.dossier / "roles.yaml").write_text(
            yaml.safe_dump(roles, allow_unicode=True, sort_keys=False), encoding="utf-8")
        horloge = itertools.count(0, 2.0)
        self.jeu = Application(configuration=Configuration(self.dossier),
                               hasard=random.Random(1348))
        self.jeu.maintenant = lambda: next(horloge)

    def _remplir(self, ouverture):
        for _ in range(40):
            vue = self.jeu.vue(ouverture["partie"], ouverture["jeton"])
        return vue

    def test_les_tailles_proposees_sont_celles_de_la_table(self):
        self.assertEqual(self.jeu.tailles_proposees(),
                         {"tailles": [6, 8], "par_defaut": 8})

    def test_sans_taille_la_partie_prend_celle_par_defaut(self):
        vue = self._remplir(self.jeu.creer_une_partie("Sonde", "sombreval"))
        self.assertEqual(vue["joueurs_attendus"], 8)
        self.assertEqual(len(vue["joueurs"]), 8)

    def test_une_partie_a_six_se_remplit_a_six_et_se_joue(self):
        ouverture = self.jeu.creer_une_partie("Sonde", "sombreval", 6)
        vue = self._remplir(ouverture)
        self.assertEqual(vue["joueurs_attendus"], 6)
        self.assertEqual(len(vue["joueurs"]), 6, "les joueurs factices s'arrêtent à six")

        self.jeu.commencer(ouverture["partie"], ouverture["jeton"])
        for _ in range(600):
            if self.jeu.vue(ouverture["partie"], ouverture["jeton"])["phase"] == "fin":
                return
        self.fail("une partie à six n'arrive pas à sa fin")

    def test_une_taille_inconnue_est_refusee_des_la_creation(self):
        with self.assertRaises(ErreurDeJeu) as refus:
            self.jeu.creer_une_partie("Sonde", "sombreval", 12)
        self.assertIn("12 joueurs", str(refus.exception))
        self.assertIn("possible : 6, 8", str(refus.exception))

    def test_la_composition_est_annoncee_par_camp(self):
        vue = self._remplir(self.jeu.creer_une_partie("Sonde", "sombreval", 6))
        camps = self.jeu.configuration.univers["sombreval"]["camps"]
        self.assertEqual(vue["composition"], [
            {"camp": camps["menace"]["nom"], "nombre": 1},
            {"camp": camps["village"]["nom"], "nombre": 5},
        ])

    def test_la_composition_ne_nomme_aucun_role(self):
        # Par camp seulement : tant que personne n'est mort, aucun nom de rôle
        # autre que le mien n'entre dans la page (décision n° 3).
        ouverture = self.jeu.creer_une_partie("Sonde", "sombreval", 6)
        self._remplir(ouverture)
        self.jeu.commencer(ouverture["partie"], ouverture["jeton"])
        vue = self.jeu.vue(ouverture["partie"], ouverture["jeton"])
        roles = self.jeu.configuration.univers["sombreval"]["roles"]
        for ligne in vue["composition"]:
            self.assertEqual(set(ligne), {"camp", "nombre"})
            self.assertNotIn(ligne["camp"], {r["nom"] for r in roles.values()})


if __name__ == "__main__":
    unittest.main()
