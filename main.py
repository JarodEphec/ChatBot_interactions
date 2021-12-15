import socket
import subprocess
from datetime import datetime
from pymongo import MongoClient
from src.config import config

# tableau avec les mots-clés
mots = ['up', 'stat', 'add', 'del', 'addTo', 'shRole', 'shPerm', "ShUtiRole", 'help']
desc = ['affiche le statut du réseau', 'affiche le nombre d’utilisateurs total',
        'ajouter un rôle à un utilisateur (Ex:add role utilisateur)', ' retirer un rôle à un utilisateur '
                                                                      '(Ex:del role utilisateur)',
        'ajouter un rôle à tous les noms utilisateurs (Ex:addTo role utilisateur1 utilisateur2)',
        'affiche une liste des différents rôles', 'affiche les permissions d\'un role (Ex:shPerm role)',
        'affiche une liste des utilisateurs par rôle (Ex: ShUtiRole role)', 'affiche toutes les commandes']


def main():
    class Command:
        def __init__(self):
            self.name = ''
            self.param = list()
            self.time = datetime

        def get_name(self):
            choice = str(input('Choissisez un mot-clé :')).lower()
            com = choice.split()
            self.name = com[0]
            for x in com[1:]:
                self.param.append(x)
            self.time = datetime.now()

    class LocalMachineCommand:
        @staticmethod
        def get_data(self):
            return self

    class NetworkStatCommand:
        @staticmethod
        def get_masque(self):  # Fonction qui renvoie le masque de sous-réseau de l'adresse ipv4
            ip = ''
            network = NetworkStatCommand()
            if self == 'local':
                ip = network.get_ipv4_local()
            elif self == 'public':
                ip = network.get_ipv4_public()
            else:
                print('Error, bad param')
            proc = subprocess.Popen('ipconfig',
                                    stdout=subprocess.PIPE)  # Fonction qui exécuter ipconfig et crée un pipe
            while True:  # on parcourt le pipe
                line = proc.stdout.readline()
                if ip.encode() in line:  # On retrouve la ligne avec l'adresse ipv4 local récupérée avant
                    break
            netmask = proc.stdout.readline().rstrip().split(b':')[-1].replace(b' ',
                                                                              b'').decode()
            # On retire les caractères et extrait le masque de sous-réseau
            return netmask

        def get_ipv4_local(self):  # Fonction qui renvoie l'adresse ipv4 local
            ip4 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Création du socket IPV4
            ip4.connect(("8.8.8.8", 80))  # Connexion à l'adresse 8.8.8.8 de google et on regarde le port 80
            return ip4.getsockname()[0]

        def get_ipv6_local(self):  # Fonction qui renvoie l'adresse ipv6 local
            try:
                ip6 = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)  # Création du socket IPV6
                ip6.connect(("2001:4860:4860::8888",
                             80))  # Connexion à l'adresse 2001:4860:4860::8888 de google et on regarde le port 80
                return ip6.getsockname()[0]
            except Exception:
                return 'Pas d\'adresse ipv6'

        def get_ipv4_public(self):  # Fonction qui renvoie l'adresse ipv4 public
            ipv4 = str(socket.gethostbyname(socket.gethostname()))
            return ipv4

        def get_ping(self):
            return print('En cours de construction...')

    class DataBaseCommand:
        """
            Cette classe permet de créer une connexion vers la base de données.
        """

        def __init__(self):
            certificat_path = config.ROOT_DIR + "\\2TM1-G2.pem"
            uri = "mongodb+srv://cluster0.5i6qo.gcp.mongodb.net/ephecom?authSource=%24external&authMechanism=MONGODB-X509"
            client = MongoClient(uri,
                                 tls=True,
                                 tlsCertificateKeyFile=certificat_path)
            self.db = client['ephecom']

        def __enter__(self):
            return self

        def __exit__(self):
            self.db.close()

    class RoleManagementCommand:
        """Role management"""

        def __init__(self, role=None, user=None):
            self.__role = role
            self.__user = user

        @property
        def role(self):
            return self.__role

        @role.setter
        def role(self, value):
            self.__role = value

        @property
        def user(self):
            return self.__user

        @user.setter
        def user(self, value):
            self.__user = value

        def add(self):
            try:
                with DataBaseCommand() as connector:
                    collection = connector.db["users"]
                    list_users = collection.find()
                    for users in list_users:
                        if self.__user == users['user_name'] and (self.__role or int(self.__role) not in
                                                                  users['list_role']):
                            new_value = {"$push": {"list_role": int(self.__role)}}
                            connector.db["users"].update_one({'user_name': self.__user}, new_value)
            except Exception as e:
                print(e)

        def dell(self):
            try:
                with DataBaseCommand() as connector:
                    collection = connector.db["users"]
                    list_users = collection.find()
                    for users in list_users:
                        if self.__user == users['user_name'] and (int(self.__role) or self.__role in
                                                                  users['list_role']):
                            users['list_role'].remove(int(self.__role))
                            del_value = {"$set": {"list_role": users['list_role']}}
                            connector.db["users"].update_one({'user_name': self.__user}, del_value)
            except Exception as e:
                print(e)

        def add_to(self):
            try:
                with DataBaseCommand() as connector:
                    collection = connector.db["users"]
                    list_users = collection.find()
                    for users in list_users:
                        if users['user_name'] in self.__user:
                            if self.__role or int(self.__role) not in users['list_role']:
                                new_value = {"$push": {"list_role": int(self.__role)}}
                                connector.db["users"].update_one({'user_name': users['user_name']}, new_value)
            except Exception as e:
                print(e)

        def show_role(self):
            try:
                with DataBaseCommand() as connector:
                    collection = connector.db["roles"]
                    list_role = collection.find()
                    for role in list_role:
                        print("Roles:", role['name'])
            except Exception as e:
                print(e)

        def show_perm(self):
            try:
                with DataBaseCommand() as connector:
                    collection = connector.db["roles"]
                    collection2 = connector.db["permissions"]
                    list_role = collection.find()
                    list_perm = collection2.find()
                    for role in list_role:
                        if role['name'] == self.__role:
                            print("Permission:", role['perm_list'])
                    for perm in list_perm:
                        print("Permission:", perm['name'])
            except Exception as e:
                print(e)

        def show_user_role(self):
            try:
                with DataBaseCommand() as connector:
                    collection = connector.db["users"]
                    user_list = []
                    list_user = collection.find()
                    for user in list_user:
                        if int(self.__role) in user['list_role']:
                            user_list.append(user['user_name'])
                    print('utilisateur ayant le role', self.__role, ":", end=' ')
                    print(', '.join(user_list))
            except Exception as e:
                print(e)

    def help():
        print('Liste des Commandes:')
        i = 0
        for cmd in mots:
            print(' ', cmd, '-', desc[i])
            i += 1

    class Result:

        def get_space(self):  # Fonction qui fait une ligne d'espace en console
            return print('')

        def display_result(self):  # Fonction d'affichage
            space = Result()
            local = LocalMachineCommand()
            network = NetworkStatCommand()
            role_cmd = RoleManagementCommand()
            # Affichage des messages de bienvenu
            print('Bienvenu dans le Chatbot')
            space.get_space()
            print('Vous pouvez tapez des mots-clés pour avoir accès à vos données réseaux')
            print('Pour mettre fin à la discussion tapez : fin')

            flag = False  # On définit un flag pour aider à boucler

            while not flag:
                com = Command()
                space.get_space()
                com.get_name()
                choice = com.name
                space.get_space()
                try:
                    if choice == 'up':
                        print('LOCAL ADDRESS :')
                        print('IPV4 ADDRESS :', local.get_data(network.get_ipv4_local()), '/',
                              local.get_data(network.get_masque('local')))  # Affichage de l'adresse IPV4 local
                        print('IPV6 ADDRESS :',
                              local.get_data(network.get_ipv6_local()))  # Affichage de l'adresse IPV6 local
                        space.get_space()
                        print('PUBLIC ADDRESS :')
                        print('IPV4 ADDRESS :', local.get_data(network.get_ipv4_public()), '/',
                              local.get_data(network.get_masque('public')))  # Affichage de l'adresse IPV4 public
                        space.get_space()
                        print('PING :')
                        local.get_data(network.get_ping())
                        space.get_space()
                    elif choice == 'stat':
                        count = 0
                        try:
                            with DataBaseCommand() as connector:
                                collection = connector.db["users"]
                                col = collection.find()
                                for i in col:
                                    count += 1
                                print('Il y a ' + str(count) + ' utilisateur(s).')
                            space.get_space()
                        except Exception as e:
                            print(e)
                    elif choice == 'add':
                        role_cmd.role = com.param[0]
                        role_cmd.user = com.param[1]
                        role_cmd.add()
                    elif choice == 'del':
                        role_cmd.role = com.param[0]
                        role_cmd.user = com.param[1]
                        role_cmd.dell()
                    elif choice == 'addto':
                        role_cmd.role = com.param[0]
                        role_cmd.user = com.param[1:]
                        role_cmd.add_to()
                    elif choice == 'shrole':
                        role_cmd.show_role()
                    elif choice == 'shperm':
                        role_cmd.role = com.param[0]
                        role_cmd.show_perm()
                    elif choice == 'shutirole':
                        role_cmd.role = com.param[0]
                        role_cmd.show_user_role()
                    elif choice == 'help':
                        help()
                    elif choice == 'check':
                        try:
                            with DataBaseCommand() as connector:
                                collection = connector.db["users"]
                                list_users = collection.find()
                                for users in list_users:
                                    print("user:", users)
                        except Exception as e:
                            print(e)
                    elif choice == 'fin':  # On passe le flag à true ça finit la boucle si l'utilisateur tape 'fin'
                        print('Merci d\'avoir utilisé le Chabot')
                        flag = True
                    else:
                        print('Choissisez une des commandes suivantes : up, stat, add, addTo, del, shRole, shPerm, '
                              'ShUtiRole, Help')
                except IndexError:
                    print('Veuillez entrée les arguments nécessaire')

    res = Result()
    res.display_result()


if __name__ == "__main__":
    main()
