import unittest
import main

class BotTestCase(unittest.TestCase):
    def test_bot_statUsers(self):
        """Vérification de statUsers"""
        self.assertEqual(main.UserStatCommand("statUsers").stat(), 'Il y a 2 utilisateur(s).')
    def test_bot_showutirole(self):
        """Vérification de showutirole"""
        self.assertEqual(main.RoleManagementCommand("showutirole 1").show_user_role(), 'utilisateur ayant le '
                                                                                       'role 1:simon, raphael')
        self.assertEqual(main.RoleManagementCommand("showutirole 2").show_user_role(), 'utilisateur ayant'
                                                                                       ' le role 2:raphael')
        self.assertRaises(TypeError, main.RoleManagementCommand("showutirole 0").show_user_role())

        self.assertRaises(TypeError, main.RoleManagementCommand("showutirole 3").show_user_role())
    #def test_bot_statspam(self):
     #   """Vérification de statspam"""
      #  self.assertEqual(main.UserStatCommand("statspam").stat_spam(), 'Top spam: Moi avec 1 messages !')
