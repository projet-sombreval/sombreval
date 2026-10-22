"""Un univers pas encore écrit se charge, s'affiche et se joue.

Avant `regles/defauts.yaml`, le moteur lisait les clés d'un univers en
indexation dure : la première manquante arrêtait le serveur. Un monde ne
pouvait donc être montré qu'une fois fini. Ces tests fixent l'inverse.
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

# Un univers réduit à ce qu'un fichier doit porter pour exister : son nom
# court, son titre, et le drapeau qui dit qu'on peut y jouer. Rien d'autre.
UNIVERS_NU = {"nom": "vide", "titre": "Monde Vide", "disponible": True}


class TestUnUniversIncomplet(unittest.TestCase):

    def setUp(self):
        """Un dossier regles/ complet, SAUF l'univers, réduit à son nom.

        On recopie les vrais fichiers de mécanique : ce qu'on éprouve est
        l'absence de CONTENU d'univers, pas une configuration bricolée.
        """
        self.dossier = Path(tempfile.mkdtemp())
        for nom in ("roles.yaml", "partie.yaml", "defauts.yaml"):
            shutil.copy(DOSSIER_REGLES / nom, self.dossier / nom)
        (self.dossier / "univers").mkdir()
        self._ecrire_univers(UNIVERS_NU)

    def tearDown(self):
        shutil.rmtree(self.dossier)

    def _ecrire_univers(self, donnees):
        chemin = self.dossier / "univers" / f"{donnees['nom']}.yaml"
        chemin.write_text(yaml.safe_dump(donnees, allow_unicode=True), encoding="utf-8")
        return chemin

    def _jeu(self):
        """Une application sur ce dossier, avec un hasard semé et une horloge."""
        horloge = itertools.count(0, 2.0)
        jeu = Application(
            configuration=Configuration(self.dossier), hasard=random.Random(1348)
        )
        jeu.maintenant = lambda: next(horloge)
        return jeu

    def test_un_univers_reduit_a_son_nom_se_charge(self):
        configuration = Configuration(self.dossier)
        univers = configuration.univers_choisi("vide")

        self.assertEqual(univers["titre"], "Monde Vide")
        for cle in ("presentation", "couleurs", "camps", "roles", "textes",
                    "messages", "pseudos_factices"):
            self.assertIn(cle, univers, f"« {cle} » devrait être comblée")

    def test_les_sept_couleurs_sont_comblees(self):
        univers = Configuration(self.dossier).univers_choisi("vide")

        self.assertEqual(
            set(univers["couleurs"]),
            {"fond", "parchemin", "encre", "encre-pale",
             "accent", "accent-clair", "bordure"},
        )

    def test_la_vue_ne_plante_pas_et_montre_les_trous(self):
        """C'est LE test du lot : avant, cette vue levait KeyError."""
        jeu = self._jeu()
        ouverture = jeu.creer_une_partie("Sonde", "vide")

        vue = jeu.vue(ouverture["partie"], ouverture["jeton"])

        self.assertEqual(vue["univers"]["presentation"], "à écrire")
        self.assertEqual(len(vue["univers"]["couleurs"]), 7)

    def test_une_partie_entiere_se_joue_sur_un_univers_vide(self):
        jeu = self._jeu()
        ouverture = jeu.creer_une_partie("Sonde", "vide")
        for _ in range(60):
            jeu.vue(ouverture["partie"], ouverture["jeton"])

        jeu.commencer(ouverture["partie"], ouverture["jeton"])
        phases = []
        for _ in range(400):
            vue = jeu.vue(ouverture["partie"], ouverture["jeton"])
            if not phases or phases[-1] != vue["phase"]:
                phases.append(vue["phase"])
            if vue["phase"] == "fin":
                break

        self.assertEqual(phases[0], "decouverte")
        self.assertEqual(phases[-1], "fin")
        self.assertIn("nuit", phases)
        self.assertIn("jour", phases)

    def test_un_univers_deja_ecrit_n_est_pas_touche(self):
        """Les valeurs de l'univers écrasent les défauts, jamais l'inverse."""
        self._ecrire_univers(
            UNIVERS_NU | {"presentation": "Un monde bien à lui.",
                          "couleurs": {"fond": "#001122"}}
        )

        univers = Configuration(self.dossier).univers_choisi("vide")

        self.assertEqual(univers["presentation"], "Un monde bien à lui.")
        self.assertEqual(univers["couleurs"]["fond"], "#001122")
        # et le reste du bloc est quand même comblé : la fusion est profonde
        self.assertEqual(univers["couleurs"]["encre"], "#1f1f1f")

    def test_les_textes_optionnels_d_un_role_restent_ABSENTS(self):
        """Un rôle qui ne révèle rien doit continuer à ne rien révéler.

        `texte_du_role()` lit `confirmation` et `revelation` avec `.get()` :
        les combler ferait parler des rôles muets, dans TOUS les univers.
        """
        univers = Configuration(self.dossier).univers_choisi("vide")

        for nom, role in univers["roles"].items():
            with self.subTest(role=nom):
                self.assertNotIn("confirmation", role)
                self.assertNotIn("revelation", role)

    def test_la_vue_dit_ce_qui_reste_a_ecrire(self):
        """L'écran doit pouvoir montrer les trous : il lui faut la liste."""
        jeu = self._jeu()
        ouverture = jeu.creer_une_partie("Sonde", "vide")

        vue = jeu.vue(ouverture["partie"], ouverture["jeton"])

        a_ecrire = vue["univers"]["a_ecrire"]
        self.assertIn("presentation", a_ecrire)
        self.assertIn("textes.attente_titre", a_ecrire)
        self.assertIn("couleurs.encre", a_ecrire)
        # une FEUILLE par trou, jamais le bloc entier : c'est texte par texte
        # que les équipes avancent.
        self.assertNotIn("textes", a_ecrire)

    def test_un_univers_complet_n_a_rien_a_ecrire(self):
        """Sombreval est écrit : sa liste doit être VIDE.

        Sans cette moitié-là, une liste qui renverrait tout marquerait aussi
        les textes déjà écrits — et le signal ne voudrait plus rien dire.
        """
        configuration = Configuration()

        self.assertEqual(configuration.univers["sombreval"]["a_ecrire"], [])

    def test_une_cle_ecrite_sort_de_la_liste(self):
        self._ecrire_univers(UNIVERS_NU | {"presentation": "Un monde bien à lui."})

        a_ecrire = Configuration(self.dossier).univers_choisi("vide")["a_ecrire"]

        self.assertNotIn("presentation", a_ecrire)
        self.assertIn("textes.attente_titre", a_ecrire)

    def test_il_y_a_assez_de_pseudonymes_pour_la_plus_grande_partie(self):
        """Mesuré : un seul pseudonyme plafonne le village à deux joueurs.

        Les joueurs factices prennent un pseudonyme NON DÉJÀ PRIS. S'il en
        manque, la partie refuse de démarrer sur un message qui accuse le
        village — et pas ce fichier-là.
        """
        configuration = Configuration(self.dossier)
        univers = configuration.univers_choisi("vide")
        plus_grande = max(configuration.compositions)

        self.assertGreaterEqual(len(univers["pseudos_factices"]), plus_grande - 1)
