import unittest
import main

class BotTestCase(unittest.TestCase):
    def test_bot_statUsers(self):
        """Vérification de statUsers"""
        self.assertEqual(main.UserStatCommand("statUsers").stat(), 'Il y a 3 utilisateur(s).')
    def test_bot_showutirole(self):
        """Vérification de showutirole"""
        self.assertEqual(main.RoleManagementCommand("showutirole 50").show_user_role(), 'utilisateur ayant le role 50:'
                                                                                     'totototo, rachiid007, '
                                                                                     'ChaosArnhug')
        self.assertEqual(main.RoleManagementCommand("showutirole 25").show_user_role(), 'utilisateur ayant le role 25:'
                                                                                        'totototo, rachiid007, '
                                                                                        'ChaosArnhug')
        self.assertEqual(main.RoleManagementCommand("showutirole 22").show_user_role(), 'utilisateur ayant le role 22:'
                                                                                        'totototo, rachiid007, '
                                                                                        'ChaosArnhug')
    def test_bot_statspam(self):
        """Vérification de statspam"""
        self.assertEqual(main.UserStatCommand("statspam").stat_spam(), 'Top spam: Moi avec 1 messages !')
