"""Les couleurs d'un univers doivent rester lisibles.

Chaque monde apporte ses sept couleurs (D1), et site.css les emploie telles
quelles. Un monde dont l'encre ne se lit pas sur le parchemin rendrait TOUS
ses écrans illisibles, sans qu'aucune ligne de code n'ait changé. Ces tests
vérifient les trois univers tels que le jeu les charge — complétés par
regles/defauts.yaml, comme à l'écran.

Le calcul est celui des règles d'accessibilité (WCAG 2) : luminance relative
de chaque couleur, puis (claire + 0,05) / (sombre + 0,05).
"""

import unittest

from jeu.configuration import Configuration

# Le seuil du texte courant. En dessous, c'est un défaut, pas un goût.
SEUIL_TEXTE = 4.5


def luminance(couleur):
    """Luminance relative d'une couleur écrite « #rrggbb »."""
    hexa = couleur.lstrip("#")
    canaux = [int(hexa[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    lineaires = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
                 for c in canaux]
    return 0.2126 * lineaires[0] + 0.7152 * lineaires[1] + 0.0722 * lineaires[2]


def contraste(a, b):
    """Rapport de contraste entre deux couleurs, de 1 à 21."""
    claire, sombre = sorted((luminance(a), luminance(b)), reverse=True)
    return (claire + 0.05) / (sombre + 0.05)


def defauts_de_lisibilite(couleurs):
    """Ce qui ne va pas dans ces sept couleurs — une liste vide si tout va."""
    defauts = []
    if luminance(couleurs["parchemin"]) <= luminance(couleurs["fond"]):
        defauts.append("--parchemin n'est pas plus clair que --fond : "
                       "la carte ne se détache plus de la page")
    ratio = contraste(couleurs["encre"], couleurs["parchemin"])
    if ratio < SEUIL_TEXTE:
        defauts.append(f"--encre contre --parchemin : {ratio:.2f}:1, "
                       f"sous le seuil de {SEUIL_TEXTE}:1")
    return defauts


class TestLesCouleursDesUnivers(unittest.TestCase):

    def test_les_trois_univers_sont_lisibles(self):
        univers = Configuration().univers
        # Sans cette garde, un dossier vide rendrait le test vert sans rien
        # avoir vérifié.
        self.assertEqual(len(univers), 3)
        for nom, donnees in univers.items():
            with self.subTest(univers=nom):
                self.assertEqual(defauts_de_lisibilite(donnees["couleurs"]), [])


class TestLaSondeMord(unittest.TestCase):
    """La sonde doit refuser une palette illisible : sinon elle ne garde rien."""

    BONNE = {"fond": "#141110", "parchemin": "#efe6d6", "encre": "#241d16"}

    def test_le_calcul_donne_les_valeurs_connues(self):
        self.assertAlmostEqual(contraste("#000000", "#ffffff"), 21.0, places=2)
        self.assertAlmostEqual(contraste("#241d16", "#efe6d6"), 13.44, places=2)

    def test_une_bonne_palette_passe(self):
        self.assertEqual(defauts_de_lisibilite(self.BONNE), [])

    def test_une_encre_trop_claire_est_refusee(self):
        palette = dict(self.BONNE, encre="#a89a86")
        self.assertIn("--encre contre --parchemin", defauts_de_lisibilite(palette)[0])

    def test_un_parchemin_plus_sombre_que_le_fond_est_refuse(self):
        palette = dict(self.BONNE, fond="#efe6d6", parchemin="#141110",
                       encre="#efe6d6")
        self.assertIn("--parchemin n'est pas plus clair",
                      defauts_de_lisibilite(palette)[0])


if __name__ == "__main__":
    unittest.main()
