"""Chaque fichier d'univers se lit, se charge et se joue jusqu'au bout.

Ce test tombera POUR DE VRAI : le jour où une ambassadrice ouvre son monde
dans l'éditeur de GitHub, une indentation de travers suffit. Son message
d'échec est donc écrit pour elle, pas pour nous : le fichier, la ligne ou la
clé en cause, et une phrase qu'une élève de seconde comprend sans aide.
Il remonte tel quel dans le résumé de la vérification « contrastes et tests ».

Les trois pièges, mesurés sur une copie de sombreval.yaml :
- une ligne mal indentée, ou une tabulation : YAML le signale à la bonne
  ligne ;
- un deux-points collé à sa valeur (`encre:"#241d16"`) : YAML le signale UNE
  LIGNE PLUS BAS — d'où « ou celle juste au-dessus » ;
- une couleur sans guillemets (`encre: #241d16`) : AUCUNE erreur, le `#`
  ouvre un commentaire et la couleur devient vide en silence. C'est le plus
  probable des trois, et seul ce test l'attrape.

Chaque monde est joué SEUL, forcé disponible, dans un dossier à part : un
fichier cassé ne doit pas faire tomber le test des deux autres.
"""

import itertools
import random
import re
import shutil
import tempfile
import unittest
from pathlib import Path

import yaml

from jeu.application import Application
from jeu.configuration import DOSSIER_REGLES, Configuration

FICHIERS = sorted((DOSSIER_REGLES / "univers").glob("*.yaml"))
COULEURS = ("fond", "parchemin", "encre", "encre-pale", "accent",
            "accent-clair", "bordure")
HEXA = re.compile(r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")

# Autant de pseudonymes que la plus grande partie compte de joueurs, moins
# l'humain. En dessous, les joueurs factices ne remplissent pas le village et
# la partie refuse de démarrer — avec un message du moteur qui accuse le
# village, pas le fichier. D'où une phrase à nous, avant.
#
# Le seuil SUIT la table de regles/roles.yaml : sept tant qu'elle s'arrête à
# huit joueurs, onze le jour où elle va jusqu'à douze (séance 9).
PSEUDOS_MINIMUM = max(Configuration().compositions) - 1


def chemin(fichier):
    return f"regles/univers/{fichier.name}"


def lire_ou_expliquer(fichier):
    """Le contenu du fichier, ou la phrase qui dit à l'élève quoi corriger."""
    try:
        donnees = yaml.safe_load(fichier.read_text(encoding="utf-8"))
    except yaml.YAMLError as erreur:
        repere = getattr(erreur, "problem_mark", None)
        ligne = repere.line + 1 if repere else None
        if "'\\t'" in str(erreur) and ligne:
            return None, (f"Le fichier {chemin(fichier)} ne se lit pas : il y a "
                          f"une tabulation à la ligne {ligne}. Remplace-la par "
                          f"des espaces.")
        ou = f"regarde la ligne {ligne}, ou celle juste au-dessus" if ligne \
            else "regarde les lignes que tu as modifiées"
        return None, (f"Le fichier {chemin(fichier)} ne se lit pas : {ou}. "
                      f"Vérifie les espaces au début de la ligne (aligne-la "
                      f"comme dans sombreval.yaml) et l'espace après chaque "
                      f"deux-points.")
    if not isinstance(donnees, dict):
        return None, (f"Le fichier {chemin(fichier)} ne se lit pas : il doit "
                      f"commencer par « nom: {fichier.stem} », comme "
                      f"sombreval.yaml.")
    return donnees, None


def defaut_de_contenu(fichier, donnees):
    """Ce qui se lit mais ne marchera pas — ou None si tout va bien."""
    if donnees.get("nom") != fichier.stem:
        return (f"Dans {chemin(fichier)}, la ligne « nom: » doit dire "
                f"{fichier.stem}, pas {donnees.get('nom')}. C'est par ce nom "
                f"que le jeu reconnaît ton monde.")
    titre = donnees.get("titre") or fichier.stem
    souci = defaut_de_couleur(titre, donnees.get("couleurs"))
    if souci:
        return souci
    if "pseudos_factices" in donnees:
        pseudos = donnees["pseudos_factices"]
        if not isinstance(pseudos, list):
            return (f"Dans le fichier de {titre}, « pseudos_factices: » doit "
                    f"être suivie d'une liste, un pseudonyme par ligne, chacun "
                    f"précédé de « - », comme dans sombreval.yaml.")
        differents = {str(p).strip() for p in pseudos if p is not None and str(p).strip()}
        if len(differents) < PSEUDOS_MINIMUM:
            return (f"Dans le fichier de {titre}, il faut au moins "
                    f"{PSEUDOS_MINIMUM} pseudonymes différents, et il y en a "
                    f"{len(differents)}. En dessous, la partie refuse de "
                    f"démarrer.")
    return None


def defaut_de_couleur(titre, couleurs):
    """La première couleur que le jeu ne pourra pas lire — ou None."""
    if couleurs is None:
        return None
    if not isinstance(couleurs, dict):
        return (f"Dans le fichier de {titre}, « couleurs: » doit être suivie "
                f"des sept couleurs, une par ligne, décalées de deux espaces, "
                f"comme dans sombreval.yaml.")
    for nom in COULEURS:
        if nom not in couleurs:
            continue
        valeur = couleurs[nom]
        if valeur is None:
            return (f"Dans le fichier de {titre}, la couleur {nom} est vide : "
                    f"mets-la entre guillemets, comme ceci : "
                    f"{nom}: \"#241d16\".")
        if not (isinstance(valeur, str) and HEXA.match(valeur)):
            return (f"Dans le fichier de {titre}, la couleur {nom} ne se lit "
                    f"pas ({valeur}) : écris-la en hexadécimal, entre "
                    f"guillemets, comme ceci : {nom}: \"#241d16\".")
    return None


def jouer_une_partie(dossier, nom, graine):
    """Une partie entière, de la salle d'attente à l'écran final."""
    horloge = itertools.count(0, 2.0)
    jeu = Application(configuration=Configuration(dossier),
                      hasard=random.Random(graine))
    jeu.maintenant = lambda: next(horloge)
    ouverture = jeu.creer_une_partie("Sonde", nom)
    for _ in range(60):
        jeu.vue(ouverture["partie"], ouverture["jeton"])
    jeu.commencer(ouverture["partie"], ouverture["jeton"])
    for _ in range(600):
        if jeu.vue(ouverture["partie"], ouverture["jeton"])["phase"] == "fin":
            return True
    return False


class TestChaqueUnivers(unittest.TestCase):

    def test_il_y_a_bien_trois_mondes(self):
        # Sans cette garde, un dossier vide rendrait les tests verts sans rien
        # avoir joué.
        self.assertEqual([f.stem for f in FICHIERS],
                         ["salem", "serenissime", "sombreval"])

    def test_chaque_monde_se_lit_et_se_joue_jusqu_au_bout(self):
        for fichier in FICHIERS:
            with self.subTest(univers=fichier.stem):
                donnees, souci = lire_ou_expliquer(fichier)
                if souci is None:
                    souci = defaut_de_contenu(fichier, donnees)
                if souci:
                    self.fail(souci)

                titre = donnees.get("titre") or fichier.stem
                dossier = Path(tempfile.mkdtemp())
                self.addCleanup(shutil.rmtree, dossier)
                for regle in ("roles.yaml", "partie.yaml", "defauts.yaml"):
                    shutil.copy(DOSSIER_REGLES / regle, dossier / regle)
                (dossier / "univers").mkdir()
                # Forcé disponible : on joue le monde tel qu'il sera le jour
                # où son équipe l'allume, pas tel qu'il est aujourd'hui.
                (dossier / "univers" / fichier.name).write_text(
                    yaml.safe_dump(dict(donnees, disponible=True),
                                   allow_unicode=True), encoding="utf-8")

                for graine in range(3):
                    try:
                        finie = jouer_une_partie(dossier, fichier.stem, graine)
                    except KeyError as erreur:
                        self.fail(f"Le monde de {titre} se charge, mais une "
                                  f"partie s'arrête en route : il manque "
                                  f"« {erreur.args[0]} ». Compare ton fichier "
                                  f"avec sombreval.yaml.")
                    except Exception as erreur:  # noqa: BLE001 — le message est pour l'élève
                        self.fail(f"Le monde de {titre} se charge, mais une "
                                  f"partie s'arrête en route : {erreur}. "
                                  f"Compare ton fichier avec sombreval.yaml.")
                    if not finie:
                        self.fail(f"Le monde de {titre} se charge, mais une "
                                  f"partie n'arrive jamais à sa fin.")


class TestLesMessagesSontLisibles(unittest.TestCase):
    """Les pièges réels donnent une phrase juste — sinon le test ne sert à rien."""

    def setUp(self):
        self.dossier = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.dossier)
        self.base = (DOSSIER_REGLES / "univers" / "sombreval.yaml").read_text(
            encoding="utf-8").replace("nom: sombreval", "nom: salem")

    def _souci(self, texte):
        fichier = self.dossier / "salem.yaml"
        fichier.write_text(texte, encoding="utf-8")
        donnees, souci = lire_ou_expliquer(fichier)
        return souci or defaut_de_contenu(fichier, donnees)

    def _ligne(self, debut):
        return next(i for i, l in enumerate(self.base.splitlines(), 1)
                    if l.startswith(debut))

    def test_une_ligne_mal_indentee_est_situee(self):
        ligne = self._ligne('  parchemin:')
        souci = self._souci(self.base.replace('  parchemin:', '   parchemin:'))
        self.assertIn(f"la ligne {ligne}", souci)
        self.assertIn("regles/univers/salem.yaml", souci)

    def test_une_tabulation_est_nommee(self):
        ligne = self._ligne('  parchemin:')
        souci = self._souci(self.base.replace('  parchemin:', '\tparchemin:'))
        self.assertIn(f"une tabulation à la ligne {ligne}", souci)

    def test_un_deux_points_colle_est_situe_a_une_ligne_pres(self):
        ligne = self._ligne('  encre:')
        souci = self._souci(self.base.replace('  encre: "', '  encre:"'))
        self.assertTrue(f"la ligne {ligne}," in souci
                        or f"la ligne {ligne + 1}," in souci, souci)
        self.assertIn("juste au-dessus", souci)

    def test_une_couleur_sans_guillemets_est_attrapee(self):
        souci = self._souci(self.base.replace('  encre: "#241d16"',
                                              '  encre: #241d16'))
        self.assertIn("la couleur encre est vide", souci)
        self.assertIn("guillemets", souci)

    def test_un_nom_recopie_de_sombreval_est_refuse(self):
        souci = self._souci(self.base.replace("nom: salem", "nom: sombreval"))
        self.assertIn("doit dire salem, pas sombreval", souci)

    def test_trop_peu_de_pseudonymes_est_dit_avant_que_la_partie_refuse(self):
        # Le bloc de Sombreval réduit à trois lignes, dont un doublon : le
        # moteur ne compte que des pseudonymes DIFFÉRENTS.
        texte = re.sub(r"pseudos_factices:\n(  - .*\n)+",
                       "pseudos_factices:\n  - Ana\n  - Bea\n  - Ana\n",
                       self.base)
        self.assertIn("  - Ana\n  - Bea\n  - Ana\n", texte)
        souci = self._souci(texte)
        self.assertIn(f"il faut au moins {PSEUDOS_MINIMUM} pseudonymes "
                      f"différents, et il y en a 2", souci)

    def test_le_vrai_fichier_de_sombreval_ne_signale_rien(self):
        fichier = DOSSIER_REGLES / "univers" / "sombreval.yaml"
        donnees, souci = lire_ou_expliquer(fichier)
        souci = souci or defaut_de_contenu(fichier, donnees)
        # Même phrase que le test des mondes, pour ne pas la doubler en
        # anglais (« … is not None ») dans le résumé de la vérification.
        if souci:
            self.fail(souci)

    def test_chaque_message_tient_sur_une_seule_ligne(self):
        # Le résumé de la vérification ne reprend que la PREMIÈRE ligne d'un
        # échec : une phrase coupée en deux y serait tronquée.
        for texte in (self.base.replace('  parchemin:', '   parchemin:'),
                      self.base.replace('  encre: "#241d16"', '  encre: #241d16'),
                      self.base.replace("nom: salem", "nom: sombreval")):
            self.assertNotIn("\n", self._souci(texte))


if __name__ == "__main__":
    unittest.main()
