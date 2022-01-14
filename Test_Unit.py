import unittest
import main

class BotTestCase(unittest.TestCase):
    def test_bot_construct(self):
        """Vérification du constructeur"""
        self.assertEqual(main.UserStatCommand("statUsers").stat(), ('Il y a ', '3', ' utilisateur(s).'))
