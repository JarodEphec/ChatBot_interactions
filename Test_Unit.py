import unittest
import main

class BotTestCase(unittest.TestCase):
    """
    Classe de test pour le Chatbot
    Author: R. Marto
    Date: Août 2022
    """

    def test_bot_add(self):
        """
        Test pour la méthode add
        """

        # Test si l'ajout d'un role fonctionne bien
        self.assertEqual(main.RoleManagementCommand('add admin raphael').add(), 'Le rôle a correctement été ajouté !')

        # Test si un utilisateur n'est pas fournit dans la command, cela doit faire un raise
        self.assertRaises(TypeError, main.RoleManagementCommand('add admin').add())

        # Test si un mauvais utilisateur est fournit dans la command, cela doit faire un raise
        self.assertRaises(TypeError, main.RoleManagementCommand('add admin zz').add())

        # Test si un mauvais role est fournit dans la command, cela doit faire un raise
        self.assertRaises(TypeError, main.RoleManagementCommand('add zz raphael').add())

        # Test qui supprime le role précèdement donner pour pouvoir refaire les tests
        self.assertEqual(main.RoleManagementCommand('del admin raphael').dell(), 'Le rôle a correctement été supprimé !')

    def test_bot_showutirole(self):
        """
        Test pour la méthode showutirole
        """

        # Test si l'affichage des utilisateur pour un role fonctionne bien
        self.assertEqual(main.RoleManagementCommand("showutirole admin").show_user_role(), 'utilisateur ayant le '
                                                                                       'role admin:simon')

        # Test si l'affichage des utilisateur pour un role fonctionne bien
        self.assertEqual(main.RoleManagementCommand("showutirole user").show_user_role(), 'utilisateur ayant le role'
                                                                                          ' user:simon, raphael')

        # Test si un mauvais role est fournit dans la command, cela doit faire un raise
        self.assertRaises(TypeError, main.RoleManagementCommand("showutirole 0").show_user_role())

        # Test si un mauvais role est fournit dans la command, cela doit faire un raise
        self.assertRaises(TypeError, main.RoleManagementCommand("showutirole zz").show_user_role())

        # Test si aucun role n'est fournit dans la command, cela doit faire un raise
        self.assertRaises(TypeError, main.RoleManagementCommand("showutirole").show_user_role())

    def test_bot_show_perm(self):
        """
        Test pour la méthode show_perm
        """

        # Test si l'affichage des permissions par role fonctionne bien
        self.assertEqual(main.RoleManagementCommand("showPerm admin").show_perm(), 'test')

        # Test si l'affichage des permissions par role fonctionne bien
        self.assertEqual(main.RoleManagementCommand("showPerm user").show_perm(), 'test')

        # Test si un mauvais role est fournit dans la command, cela doit faire un raise
        self.assertRaises(TypeError, main.RoleManagementCommand("showPerm 0").show_user_role())

        # Test si un mauvais role est fournit dans la command, cela doit faire un raise
        self.assertRaises(TypeError, main.RoleManagementCommand("showPerm zz").show_user_role())

        # Test si aucun role n'est fournit dans la command, cela doit faire un raise
        self.assertRaises(TypeError, main.RoleManagementCommand("showPerm").show_user_role())
