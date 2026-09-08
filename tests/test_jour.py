"""Le vote du village et la discussion."""

import unittest

from jeu.erreurs import ErreurDeJeu
from jeu.jour import MESSAGES_PAR_JOUR, dire, resoudre_le_jour, voter
from tests.fabrique import partie_pour_les_tests

COMPOSITION = ["menace", "menace"] + ["villageois"] * 4


class TestJour(unittest.TestCase):

    def setUp(self):
        self.partie = partie_pour_les_tests(COMPOSITION, phase="jour")
        self.accuse = self.partie.joueurs[0]
        self.premier, self.second = self.partie.joueurs[2], self.partie.joueurs[3]
        self.troisieme = self.partie.joueurs[4]

    def test_le_plus_accuse_est_elimine(self):
        voter(self.partie, self.premier, self.accuse.numero)
        voter(self.partie, self.second, self.accuse.numero)
        voter(self.partie, self.troisieme, self.premier.numero)

        resoudre_le_jour(self.partie)

        self.assertFalse(self.accuse.vivant)
        self.assertIn("le Loup", self.partie.journal[-1]["texte"])

    def test_une_egalite_nelimine_personne(self):
        voter(self.partie, self.premier, self.accuse.numero)
        voter(self.partie, self.second, self.premier.numero)

        resoudre_le_jour(self.partie)

        self.assertEqual(len(self.partie.vivants()), 6)
        self.assertIn("pas su choisir", self.partie.journal[-1]["texte"])

    def test_personne_ne_vote_personne_nest_elimine(self):
        resoudre_le_jour(self.partie)
        self.assertEqual(len(self.partie.vivants()), 6)

    def test_on_peut_changer_son_vote(self):
        voter(self.partie, self.premier, self.accuse.numero)
        voter(self.partie, self.premier, self.second.numero)
        self.assertEqual(self.partie.votes[self.premier.numero], self.second.numero)

    def test_on_ne_vote_pas_contre_soi_meme(self):
        with self.assertRaises(ErreurDeJeu):
            voter(self.partie, self.premier, self.premier.numero)

    def test_un_mort_ne_vote_pas(self):
        self.premier.vivant = False
        with self.assertRaises(ErreurDeJeu):
            voter(self.partie, self.premier, self.accuse.numero)

    def test_on_ne_juge_pas_un_mort(self):
        self.accuse.vivant = False
        with self.assertRaises(ErreurDeJeu):
            voter(self.partie, self.premier, self.accuse.numero)

    def test_on_ne_vote_pas_la_nuit(self):
        self.partie.phase = "nuit"
        with self.assertRaises(ErreurDeJeu):
            voter(self.partie, self.premier, self.accuse.numero)

    def test_on_ne_dit_que_les_phrases_prevues(self):
        dire(self.partie, self.premier, 0)
        self.assertEqual(
            self.partie.discussion[-1]["texte"], self.partie.univers["messages"][0]
        )

    def test_une_phrase_qui_nexiste_pas_est_refusee(self):
        with self.assertRaises(ErreurDeJeu):
            dire(self.partie, self.premier, 999)

    def test_on_ne_parle_pas_toute_la_journee(self):
        for _ in range(MESSAGES_PAR_JOUR):
            dire(self.partie, self.premier, 0)
        with self.assertRaises(ErreurDeJeu):
            dire(self.partie, self.premier, 0)


if __name__ == "__main__":
    unittest.main()
