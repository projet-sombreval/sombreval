"""Le compteur des « à écrire » : il empêche de reculer."""

# ── À TOI · GARDIENNE DU DÉPÔT ──────────────────────
# Un test qui empêche de reculer. Il compte les « à
# écrire » de chaque monde et refuse qu'il y en ait plus
# que le nombre que tu inscris. Tu baisses ce nombre à
# chaque séance ; si quelqu'un efface un texte par erreur,
# le contrôle rougit tout de suite. C'est aussi le
# compteur que la cheffe de projet lira chaque semaine.
#
# En attendant, le test ci-dessous passe et ne vérifie
# rien : c'est ce qui garde la vérification verte. Tu
# remplaces tout son contenu.
# ──────────────────────────────────────────────────────

import unittest


class TestAvancement(unittest.TestCase):

    def test_a_toi(self):
        pass


if __name__ == "__main__":
    unittest.main()
