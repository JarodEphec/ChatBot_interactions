import socket
import subprocess
import matplotlib.pyplot as plt
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from src.config import config

# tableau avec les mots-clés
mots = ['Commande Réseaux:', 'network', 'Commande Statistique:', 'statUsers', "histoCommand", "statConnected", 'statSpam', "graphMessages",
        "statChannel",
        'Commande Role:', 'add', 'del', 'addTo', 'showRole', 'showPerm',
        "ShowUtiRole", 'dbAcces', 'help']
desc = ['', 'affiche le statut du réseau', '', 'affiche le nombre d’utilisateurs total',
        'affiche l’historique de commande de l’utilisateur',
        "Nombre d'utilisateur connecter total ou par role (-role pour tout les role sauf ce role)",
        "affiche utilisateur qui spam le plus", 'Graph des message envoyer', 'Top des channel les plus actif', '',
        'ajouter un rôle à un utilisateur (Ex:add role utilisateur)', ' retirer un rôle à un utilisateur '
                                                                      '(Ex:del role utilisateur)',
        'ajouter un rôle à tous les noms utilisateurs (Ex:addTo role utilisateur1 utilisateur2)',
        'affiche une liste des différents rôles', 'affiche les permissions d\'un role (Ex:shPerm role)',
        'affiche une liste des utilisateurs par rôle (Ex: ShUtiRole role)', 'Indique si la connexion a la db a reussi',
        'affiche toutes les commandes']
histo_cmd = []


def main():
    class Command:
        """
        This class takes care of splitting the command into name and the different parameters.
        """
        def __init__(self):
            """
            This build initializes the parameters.

            PRE : -
            POST : -
            RAISES : -
            """
            self.name = ''
            self.param = ['0', '']
            self.time = datetime

        def get_name(self, sentence):
            """
            This function allows you to split the command line written by the user into different parameters.

            PRE : Sentence need to be str
            POST : Sentence is split in paramters
            RAISES : -
            """
            choice = sentence
            com = choice.split()
            self.name = com[0]
            i = 0
            for x in com[1:]:
                if i < 2:
                    self.param[i] = x
                    i += 1
                else:
                    self.param.append(x)

            self.time = datetime.now().strftime("%d-%m-%Y  %H:%M")

    class HistoCommand:
        """
        This class will store the last 50 commands entered by the user.
        """
        def __init__(self, name=None, param=None, time=None):
            """
            This build initializes the parameters.

            PRE : name is str, param is list of str and time is datetime. They are all initialize at None.
            POST : -
            RAISES : -
            """
            self.__name = name
            self.__param = param
            self.__time = time

        @property
        def name(self):
            return self.__name

        @name.setter
        def name(self, value):
            self.__name = value

        @property
        def param(self):
            return self.__param

        @param.setter
        def param(self, value):
            self.__param = value

        @property
        def time(self):
            return self.__time

        @time.setter
        def time(self, value):
            self.__time = value

        def get_histo(self):
            """
            This function adds commands entered by the user to the history.

            PRE : -
            POST : -
            RAISES : -
            """
            histo_cmd.append({"cmd": self.__name, "param": " ".join(self.__param), "time": self.__time})

    class LocalMachineCommand(Command):
        """
        This class helps to better identify local data and data from the database.
        """
        def __init__(self):
            """
            This build initializes the parameters.

            PRE : -
            POST : -
            RAISES : -
            """
            Command.__init__(self)

        @staticmethod
        def get_data(self):
            return self

    class NetworkStatCommand(LocalMachineCommand):
        """
            This class handles all network-related commands.
        """
        def __init__(self):
            """
            This function allows you to split the command line written by the user into different parameters.

            PRE : -
            POST : -
            RAISES : -
            """
            LocalMachineCommand.__init__(self)

        def get_masque(self, param):  # Fonction qui renvoie le masque de sous-réseau de l'adresse ipv4
            """
            This function will retrieve the masks linked to the IP addresses via an ipconfig.

            PRE : param is str
            POST : netmask is str
            RAISES : -
            """
            ip = ''
            if param == 'local':
                ip = self.get_ipv4_local()
            elif param == 'public':
                ip = self.get_ipv4_public()
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

        @staticmethod
        def get_ipv4_local():
            """
            This function retrieves the local ipv4 address.

            PRE : -
            POST : ipv4 is str
            RAISES : -
            """
            ip4 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            ip4.connect(("8.8.8.8", 80))
            return ip4.getsockname()[0]

        @staticmethod
        def get_ipv6_local():
            """
            This function retrieves the local ipv6 address.

            PRE : -
            POST : ipv6 is str
            RAISES : -
            """
            try:
                ip6 = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
                ip6.connect(("2001:4860:4860::8888",
                             80))
                return ip6.getsockname()[0]
            except Exception:
                return 'Pas d\'adresse ipv6'

        @staticmethod
        def get_ipv4_public():
            """
            This function retrieves the public ipv4 address.

            PRE : -
            POST : ipv4 is str
            RAISES : -
            """
            ipv4 = str(socket.gethostbyname(socket.gethostname()))
            return ipv4

        @staticmethod
        def get_ping():
            return print('En cours de construction...')

    class DataBaseCommand(Command):
        """
        This class is used to create a connection to the database.
        """
        def __init__(self):
            """
            This build initializes the parameters.

            PRE : -
            POST : -
            RAISES : -
            """
            Command.__init__(self)
            certificat_path = config.ROOT_DIR + "\\2TM1-G2.pem"
            uri = "mongodb+srv://cluster0.5i6qo.gcp.mongodb.net/" \
                  "ephecom?authSource=%24external&authMechanism=MONGODB-X509"
            client = MongoClient(uri,
                                 tls=True,
                                 tlsCertificateKeyFile=certificat_path)
            self.test_connect = client
            self.db = client['ephecom']

        def __enter__(self):
            return self

        def __exit__(self, *_):
            try:
                self.db.close()
            except Exception:
                pass

    class UserStatCommand(DataBaseCommand):
        """
        This class is used to obtain statistics about users.
        """
        def __init__(self, sentence):
            """
            This function allows you to split the command line written by the user into different parameters.

            PRE : Sentence need to be str
            POST : Role allocation and its str
            RAISES : -
            """
            DataBaseCommand.__init__(self)
            self.get_name(sentence)
            self.__role = self.param[0]

        @staticmethod
        def stat():
            """
            This function counts the total number of users.

            PRE : -
            POST : It displays number of users
            RAISES : -
            """
            count = 0
            try:
                with DataBaseCommand() as connector:
                    collection = connector.db["users"]
                    col = collection.find()
                    for i in col:
                        count += 1
                    print('Il y a ', str(count), ' utilisateur(s).')
            except Exception as e:
                print(e)

        @staticmethod
        def histo_com():
            """
            This function displays the commands entered by the user.

            PRE : -
            POST : It displays the commands with the name, parameters and time
            RAISES : -
            """
            for cmd in histo_cmd:
                print("Commande:", cmd["cmd"], cmd["param"], cmd["time"])

        @staticmethod
        def graph_mess():
            """
            This function displays the number of messages sent during the week.

            PRE : -
            POST : It displays number of messages
            RAISES : -
            """
            week = [0, 0, 0, 0, 0, 0, 0]
            try:
                with DataBaseCommand() as connector:
                    collection = connector.db["messages"]
                    list_message = collection.find()
                    for message in list_message:
                        var_time = message['timestamp']
                        week[datetime.strptime(var_time, '%Y-%m-%d %H:%M:%S.%f').weekday()] += 1
            except Exception as e:
                print(e)
            x = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'samedi', 'dimanche']
            y = [week[0], week[1], week[2], week[3], week[4], week[5], week[6]]  # replace with nb message when ready
            plt.plot(x, y, color='purple')
            plt.xlabel("jours de la semaine")
            plt.ylabel("Nombre de message")
            plt.title("Nombre de message envoyer par jour pour 1 semaine")
            plt.show()

        @staticmethod
        def stat_spam():
            """
            This function displays the user who spams the most.

            PRE : -
            POST : It displays its name
            RAISES : -
            """
            spammer_dict = {}
            try:
                with DataBaseCommand() as connector:
                    collection = connector.db["users"]
                    collection2 = connector.db["messages"]
                    list_users = collection.find()
                    list_message = collection2.find()
                    spammer_dict['Moi'] = 1
                    for users in list_users:
                        spammer_dict[users['pseudo']] = 1
                    for message in list_message:
                        var_time = message['timestamp']
                        diff = round((datetime.now() - datetime.strptime(var_time, '%Y-%m-%d %H:%M:%S.%f')
                                      ).total_seconds()/3600)
                        if diff < 20:
                            spammer_dict[message['sender']] += 1
                    spam_top = list(spammer_dict.items())
                    sorted(spam_top, key=lambda t: t[1])
                    print('Top spam:', spam_top[0][0], 'avec', spam_top[0][1], 'messages !')
            except Exception as e:
                print(e)

        def stat_co(self):
            """
            This function displays the names of the logged-in users or by their role.

            PRE : -
            POST : It displays names of the logged-in users or by their role.
            RAISES : -
            """
            try:
                with DataBaseCommand() as connector:
                    collection = connector.db["users"]
                    list_users = collection.find()
                    for users in list_users:
                        if self.__role == "-":
                            if int(self.__role) not in users["list_role"]:
                                print(users['pseudo'])
                        elif int(self.__role) in users["list_role"]:
                            print(users['pseudo'])
                        else:
                            print(users['pseudo'])
            except Exception as e:
                print(e)

        @staticmethod
        def stat_chan():
            """
            This function displays the top 3 most used channels.

            PRE : -
            POST : It displays the top 3 most used channels.
            RAISES : -
            """
            top_channel = {}
            try:
                with DataBaseCommand() as connector:
                    collection = connector.db["messages"]
                    list_message = collection.find()
                    for msg in list_message:
                        if msg['channel_id'][1] in top_channel:
                            top_channel[msg['channel_id'][1]] += 1
                        else:
                            top_channel[msg['channel_id'][1]] = 1
                    channel_top = list(top_channel.items())
                    sorted(channel_top, key=lambda t: t[1])
                    for i in range(3):
                        print('Top', i+1, 'pour le channel', channel_top[i][0], 'nombre de message:', channel_top[i][1])
            except Exception as e:
                print(e)

    class RoleManagementCommand(DataBaseCommand):
        """
        This class takes care of everything related to role management.
        """
        def __init__(self, sentence):
            """
            This function allows you to split the command line written by the user into different parameters.

            PRE : Sentence need to be str
            POST : Role, user and group assignment
            RAISES : -
            """
            DataBaseCommand.__init__(self)
            self.get_name(sentence)
            self.__role = self.param[0]
            self.__user = self.param[1]
            self.__group = self.param[1:]

            cmd_histo = HistoCommand()
            cmd_histo.name = self.name
            cmd_histo.param = self.param
            cmd_histo.time = self.time
            cmd_histo.get_histo()

        def add(self):
            """
            This function adds a role to a user in the database.

            PRE : -
            POST : The dabase is modified
            RAISES : -
            """
            try:
                with DataBaseCommand() as connector:
                    collection = connector.db["users"]
                    list_users = collection.find()
                    for users in list_users:
                        if self.__user == users['pseudo'] and (self.__role or int(self.__role) not in users['list_role']
                                                               ):
                            new_value = {"$push": {"list_role": int(self.__role)}}
                            connector.db["users"].update_one({'pseudo': self.__user}, new_value)
            except Exception as e:
                print(e)

        def dell(self):
            """
            This function delete a role to a user in the database.

            PRE : -
            POST : The dabase is modified
            RAISES : -
            """
            try:
                with DataBaseCommand() as connector:
                    collection = connector.db["users"]
                    list_users = collection.find()
                    for users in list_users:
                        if self.__user == users['pseudo'] and (int(self.__role) or self.__role in users['list_role']):
                            users['list_role'].remove(int(self.__role))
                            del_value = {"$set": {"list_role": users['list_role']}}
                            connector.db["users"].update_one({'pseudo': self.__user}, del_value)
            except Exception as e:
                print(e)

        def add_to(self):
            """
            This function adds a role to multiple users in the database.

            PRE : -
            POST : The dabase is modified
            RAISES : -
            """
            try:
                with DataBaseCommand() as connector:
                    collection = connector.db["users"]
                    list_users = collection.find()
                    for users in list_users:
                        if users['pseudo'] in self.__group:
                            if self.__role or int(self.__role) not in users['list_role']:
                                new_value = {"$push": {"list_role": int(self.__role)}}
                                connector.db["users"].update_one({'pseudo': users['pseudo']}, new_value)
            except Exception as e:
                print(e)

        @staticmethod
        def show_role():
            """
            This function displays the different roles that exist.

            PRE : -
            POST : It displays the roles
            RAISES : -
            """
            try:
                with DataBaseCommand() as connector:
                    collection = connector.db["roles"]
                    list_role = collection.find()
                    for role in list_role:
                        print("Roles:", role['name'])
            except Exception as e:
                print(e)

        def show_perm(self):
            """
            This function displays the different permissions in relation to a role.

            PRE : -
            POST : It displays the permissions
            RAISES : -
            """
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
            """
            This function displays the different users in relation to a role.

            PRE : -
            POST : It displays the users
            RAISES : -
            """
            try:
                with DataBaseCommand() as connector:
                    collection = connector.db["users"]
                    user_list = []
                    list_user = collection.find()
                    for user in list_user:
                        if int(self.__role) in user['list_role']:
                            user_list.append(user['pseudo'])
                    print('utilisateur ayant le role', self.__role, ":", end=' ')
                    print(', '.join(user_list))
            except Exception as e:
                print(e)

    def db_acces():
        """
        This function allows to check the access to the database.

        PRE : -
        POST : It displays if you have the access or not
        RAISES : -
        """
        try:
            with DataBaseCommand() as connector:
                connector.test_connect.admin.command('ismaster')
                print('Data base running')
        except ConnectionFailure:
            print("Data base not available")

    def help_str():
        print('Liste des Commandes:')
        i = 0
        for cmd in mots:
            if desc[i] == '':
                print()
                print(' ', cmd)
                print()
            else:
                print(' ', cmd, '-', desc[i])
            i += 1

    class Result:
        """
        This class is used to display the results of commands.
        """

        @staticmethod
        def get_space():
            return print('')

        @staticmethod
        def display_result():
            """
            This function is used to display the result of the commands.

            PRE : -
            POST : It displays the result
            RAISES : -
            """
            space = Result()
            print('Bienvenu dans le Chatbot')
            space.get_space()
            print('Vous pouvez tapez des mots-clés pour avoir accès à vos données réseaux')
            print('Pour mettre fin à la discussion tapez : fin')

            flag = False  # On définit un flag pour aider à boucler

            while not flag:
                data = str(input('Choissisez un mot-clé :')).lower()
                com = Command()
                space.get_space()
                com.get_name(data)
                choice = com.name
                local = LocalMachineCommand()
                network = NetworkStatCommand()
                role_cmd = RoleManagementCommand(data)
                stat = UserStatCommand(data)
                space.get_space()
                try:
                    if choice == 'network':
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
                    elif choice == 'statusers':
                        stat.stat()
                    elif choice == 'histocommand':
                        stat.histo_com()
                    elif choice == 'graphmessages':
                        stat.graph_mess()
                    elif choice == 'statspam':
                        stat.stat_spam()
                    elif choice == 'statconnected':
                        stat.stat_co()
                    elif choice == 'statchannel':
                        stat.stat_chan()
                    elif choice == 'add':
                        role_cmd.add()
                    elif choice == 'del':
                        role_cmd.dell()
                    elif choice == 'addto':
                        role_cmd.add_to()
                    elif choice == 'showrole':
                        role_cmd.show_role()
                    elif choice == 'showperm':
                        role_cmd.show_perm()
                    elif choice == 'showutirole':
                        role_cmd.show_user_role()
                    elif choice == 'dbacces':
                        db_acces()
                    elif choice == 'help':
                        help_str()

                    #à supprimer
                    elif choice == 'check':
                        try:
                            with DataBaseCommand() as connector:
                                print(connector.db.list_collection_names())
                                collection = connector.db["messages"]
                                collection2 = connector.db["channel"]
                                list_users = collection.find()
                                list_msg = collection2.find()
                                for users in list_users:
                                    print("user:", users)
                                print()
                                for msg in list_msg:
                                    print('msg:', msg)
                        except Exception as e:
                            print(e)
                    elif choice == 'fin':  # On passe le flag à true ça finit la boucle si l'utilisateur tape 'fin'
                        print('Merci d\'avoir utilisé le Chabot')
                        flag = True
                    else:
                        print('Entrée Help pour avoir une liste des commandes.')
                except IndexError:
                    print('Veuillez entrée les arguments nécessaire')

    res = Result()
    res.display_result()


if __name__ == "__main__":
    main()
