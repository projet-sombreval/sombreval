"""Tests du serveur local."""

import unittest

from jeu.serveur import DOSSIER_SITE


class TestServeur(unittest.TestCase):

    def test_le_dossier_du_site_existe(self):
        self.assertTrue(DOSSIER_SITE.is_dir())

    def test_le_site_a_une_page_d_accueil(self):
        self.assertTrue((DOSSIER_SITE / "index.html").is_file())


if __name__ == "__main__":
    unittest.main()
