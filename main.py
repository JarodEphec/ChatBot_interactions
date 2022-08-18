import socket
import subprocess
import matplotlib.pyplot as plt
import logging
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
        "nombre d'utilisateurs connectés au total ou par role (-role pour tous les roles sauf ce role)",
        "affiche utilisateur qui spam le plus", 'Graph des messages envoyés', 'top des channel les plus actif', '',
        'ajoute un rôle à un utilisateur (Ex: add role utilisateur)', ' retire un rôle à un utilisateur '
                                                                      '(Ex: del role utilisateur)',
        'ajoute un rôle à tous les noms utilisateurs (Ex: addTo role utilisateur1 utilisateur2)',
        'affiche une liste des différents rôles', 'affiche les permissions d\'un role (Ex: showPerm role)',
        'affiche une liste des utilisateurs par rôle (Ex: ShowUtiRole role)', 'indique si la connexion a la base de donnée est fonctionnelle',
        'affiche toutes les commandes']
histo_cmd = []

logging.basicConfig(filename='Function.log', encoding='utf-8', level=logging.DEBUG, format='%(levelname)s:%(message)s (%(asctime)s)', datefmt='%m/%d/%Y %I:%M:%S %p')


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
        POST : netmask is str - Retourne le masque de sous-réseau ipv4
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
        POST : ipv4 is str - Retourne l'addresse local ipv4
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
        POST : ipv6 is str - Retourne l'addresse local ipv6
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
        POST : ipv4 is str - Retourne l'addresse ipv4
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
        uri = "mongodb+srv://projet.s2dzjv7.mongodb.net/ephec?authSource=%24external&authMechanism=MONGODB-X509"
        client = MongoClient(uri,
                             tls=True,
                             tlsCertificateKeyFile=certificat_path)
        self.test_connect = client
        self.db = client['ephec']

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

        PRE : Sentence need to be a string - It is the string typed by the users in the command line
        POST : initialize self.__role
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
        POST : It returns the number of users
        RAISES : -
        """
        count = 0
        try:
            with DataBaseCommand() as connector:
                collection = connector.db["users"]
                col = collection.find()
                for i in col:
                    count += 1
                print('Il y a', str(count), 'utilisateur(s).')
        except Exception as e:
            print(e)

    @staticmethod
    def histo_com():
        """
        This function displays the commands entered by the user.

        PRE : -
        POST : It returns the commands with the name, parameters and time
        RAISES : -
        """
        for cmd in histo_cmd:
            print("Commande:", cmd["cmd"], cmd["param"], cmd["time"])

    @staticmethod
    def graph_mess():
        """
        This function displays the number of messages sent during the week.

        PRE : -
        POST : It returns number of messages
        RAISES : -
        """
        week = [0, 0, 0, 0, 0, 0, 0]
        try:
            with DataBaseCommand() as connector:
                collection = connector.db["messages"]
                list_message = collection.find()
                for message in list_message:
                    var_time = message['timestamp']
                    week[datetime.strptime(var_time, '%Y-%m-%d %H:%M:%S').weekday()] += 1
        except Exception as e:
            print(e)
        x = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'samedi', 'dimanche']
        y = [week[0], week[1], week[2], week[3], week[4], week[5], week[6]]  # replace with nb message when ready
        plt.plot(x, y, color='purple')
        plt.xlabel("jours de la semaine")
        plt.ylabel("Nombre de messages")
        plt.title("Nombre de messages envoyés par jour pour 1 semaine")
        plt.show()

    @staticmethod
    def stat_spam():
        """
        This function displays the user who spams the most.

        PRE : -
        POST : It returns its name
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
                    diff = round((datetime.now() - datetime.strptime(var_time, '%Y-%m-%d %H:%M:%S')
                                  ).total_seconds()/3600)
                    if diff/10000 < 20:
                        spammer_dict[message['sender']] += 1
                spam_top = list(spammer_dict.items())
                spam_top = sorted(spam_top, key=lambda t: t[0][1])
                print('Top spam:', spam_top[0][0], 'avec', int(spam_top[0][1])-1, 'messages !')
                return 'Top spam: ' + str(spam_top[0][0]) + ' avec ' + str(spam_top[0][1]) + ' messages !'
        except Exception as e:
            print(e)

    def stat_co(self):
        """
        This function displays the names of the logged-in users or by their role.

        PRE : -
        POST : It returns the names of the logged-in users or by their role.
        RAISES : -
        """
        try:
            with DataBaseCommand() as connector:
                collection = connector.db["users"]
                list_users = collection.find()
                collection = connector.db["roles"]
                list_role = collection.find()
                err = 0
                for role in list_role:
                    if self.__role[1:] == role['name']:
                        err = 1
                    if self.__role == '0':
                        err = 1
                if err == 1:
                    for users in list_users:
                        if self.__role[0] == "-":
                            if self.__role[1:] not in users["list_role"]:
                                print(users['pseudo'])
                        elif self.__role in users["list_role"]:
                            print(users['pseudo'])
                        else:
                            print(users['pseudo'])
                else:
                    raise ValueError(1)
        except ValueError as error:
            if error.args[0] == 1:
                print('Role not found')
                logging.info("stat co couldn't finish cause : role=" + self.__role)

    @staticmethod
    def stat_chan():
        """
        This function displays the top 3 most used channels.

        PRE : -
        POST : It returns the top 3 most used channels.
        RAISES : -
        """
        top_channel = {}
        try:
            with DataBaseCommand() as connector:
                collection = connector.db["messages"]
                list_message = collection.find()
                for msg in list_message:
                    if msg['channel_id'] is not None:
                        if msg['channel_id'] in top_channel:
                            top_channel[msg['channel_id']] += 1
                        else:
                            top_channel[msg['channel_id']] = 1
                channel_top = list(top_channel.items())
                channel_top = sorted(channel_top, key=lambda t: t[1])
                for i in range(3):
                    print('Top', i+1, 'pour le channel', channel_top[i][0], 'nombre de message:', channel_top[i][1])
                return 'Top' + str(1) + 'pour le channel' + str(channel_top[1][0]) + 'nombre de message:' + \
                       str(channel_top[1][1])
        except Exception as e:
            pass

class RoleManagementCommand(DataBaseCommand):
    """
    This class takes care of everything related to role management.
    """
    def __init__(self, sentence):
        """
        This function allows you to split the command line written by the user into different parameters.

        PRE : Sentence need to be a string - It is the string typed by the users in the command line
        POST : initialize Role, user and group
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

        PRE : Role and User need to be a string
        POST : Give a role to a user
        RAISES : ValueError(1): No parameter - ValueError(2):  User not found or missing - ValueError(3): Role not found
         or already assigned
        """
        try:
            with DataBaseCommand() as connector:
                collection = connector.db["users"]
                list_users = collection.find()
                collection = connector.db["roles"]
                list_roles = collection.find()
                err = 0
                if self.__role == '0':
                    raise ValueError(1)
                for users in list_users:
                    if self.__user == users['pseudo']:
                        err = 1
                        for roles in list_roles:
                            if (self.__role not in users['list_role']) and (self.__role == roles['name']):
                                err = 2
                                new_value = {"$push": {"list_role": self.__role}}
                                connector.db["users"].update_one({'pseudo': self.__user}, new_value)
                                print('Le rôle a correctement été ajouté !')
                                return 'Le rôle a correctement été ajouté !'
                if err == 0:
                    raise ValueError(2)
                if err == 1:
                    raise ValueError(3)
        except ValueError as error:
            if error.args[0] == 1:
                print('No Role has been entered.')
                logging.info("add couldn't finish cause : role=" + self.__role)
            if error.args[0] == 2:
                print('User Not found or missing')
                logging.info("add couldn't finish cause : role=" + self.__user)
            if error.args[0] == 3:
                print('Role not found or already assigned')
                logging.info("add couldn't finish cause : role=" + self.__role)

    def dell(self):
        """
        This function delete a role to a user in the database.

        PRE : Role and User need to be a string
        POST : delete a role to a user
        RAISES : ValueError(1): No parameter - ValueError(2):  User not found or missing - ValueError(3): Role not found
        """
        try:
            with DataBaseCommand() as connector:
                collection = connector.db["users"]
                list_users = collection.find()
                collection = connector.db["roles"]
                list_roles = collection.find()
                err = 0
                if self.__role == '0':
                    raise ValueError(1)
                for users in list_users:
                    if self.__user == users['pseudo']:
                        err = 1
                        for roles in list_roles:
                            if (self.__role in users['list_role']) and (self.__role == roles['name']):
                                err = 2
                                users['list_role'].remove(self.__role)
                                del_value = {"$set": {"list_role": users['list_role']}}
                                connector.db["users"].update_one({'pseudo': self.__user}, del_value)
                                print('Le rôle a correctement été supprimé !')
                                return 'Le rôle a correctement été supprimé !'
                if err == 0:
                    raise ValueError(2)
                if err == 1:
                    raise ValueError(3)
        except ValueError as error:
            if error.args[0] == 1:
                print('No Role has been entered.')
                logging.info("del couldn't finish cause : role=" + self.__role)
            if error.args[0] == 2:
                print('User Not found or missing')
                logging.info("del couldn't finish cause : role=" + self.__user)
            if error.args[0] == 3:
                print('Role not found')
                logging.info("del couldn't finish cause : role=" + self.__role)

    def add_to(self):
        """
        This function adds a role to multiple users in the database.

        PRE : Role need to be a string and group need to be a list(string)
        POST : Give a role to multiple users
        RAISES : ValueError(1): No parameter - ValueError(2):  role not found - ValueError(3): Users incorrect
        """
        try:
            with DataBaseCommand() as connector:
                collection = connector.db["users"]
                list_users = collection.find()
                collection = connector.db["roles"]
                list_roles = collection.find()
                if self.__role == '0':
                    raise ValueError(1)
                err = 0
                for roles in list_roles:
                    if self.__role in roles['name']:
                        err = 1
                        for users in list_users:
                            if (self.__role not in users['list_role']) and (users['pseudo'] in self.__group):
                                err = 2
                                new_value = {"$push": {"list_role": self.__role}}
                                connector.db["users"].update_one({'pseudo': users['pseudo']}, new_value)
                                print('Le rôle a correctement été ajouté aux utilisateurs !')
                if err == 0:
                    raise ValueError(2)
                if err == 1:
                    raise ValueError(3)
        except ValueError as error:
            if error.args[0] == 1:
                print('No Role has been entered.')
                logging.info("add to couldn't finish cause : role=" + self.__role)
            if error.args[0] == 2:
                print('Role not found')
                logging.info("add to couldn't finish cause : role=" + self.__role)
            if error.args[0] == 3:
                print('Users entered incorrect')

    @staticmethod
    def show_role():
        """
        This function displays the different roles that exist.

        PRE : -
        POST : It returns the roles
        RAISES : -
        """
        try:
            with DataBaseCommand() as connector:
                collection = connector.db["roles"]
                list_role = collection.find()
                for role in list_role:
                    print("Role",role['id'],":", role['name'])
        except Exception as e:
            print(e)

    def show_perm(self):
        """
        This function displays the different permissions in relation to a role.

        PRE : Role need to be a string
        POST : It returns the permissions of a role
        RAISES : ValueError(1): No role entered - ValueError(2): Role not found
        """
        try:
            with DataBaseCommand() as connector:
                collection = connector.db["roles"]
                collection2 = connector.db["permissions"]
                list_role = collection.find()
                list_perm = collection2.find()
                if self.__role == '0':
                    raise ValueError(1)
                err = 0
                for role in list_role:
                    if role['name'] == self.__role:
                        err = 1
                        print("Role:", self.__role)
                        print("Permission: N°", role['perm_list'][0])
                        for perm in list_perm:
                            print("Permission:", perm['name'])
                            return perm['name']
                if err == 0:
                    raise ValueError(2)
        except ValueError as error:
            if error.args[0] == 1:
                print('No Role has been entered.')
                logging.info("Show perm couldn't finish cause : role="+ self.__role)
            if error.args[0] == 2:
                print('Role not found')
                logging.info("Show perm couldn't finish cause : role=" + self.__role)

    def show_user_role(self):
        """
        This function displays the different users in relation to a role.

        PRE : Role need to be a string
        POST : It returns the users that have a specific role
        RAISES : ValueError(1): No role entered - ValueError(2): Role not found or no one possesses it
        """
        try:
            with DataBaseCommand() as connector:
                collection = connector.db["users"]
                user_list = []
                list_user = collection.find()
                if self.__role == '0':
                    raise ValueError(1)
                for user in list_user:
                    if self.__role in user['list_role']:
                        user_list.append(user['pseudo'])
                if user_list != []:
                    print('utilisateur ayant le role', self.__role, ":", end=' ')
                    print(', '.join(user_list))
                    return 'utilisateur ayant le role ' + self.__role + ":" + ', '.join(user_list)
                raise ValueError(2, "No one has role number ", self.__role, " or it doesn't exist")
        except ValueError as error:
            if error.args[0] == 1:
                print("No Role has been entered.")
                logging.debug("Show user role couldn't finish cause : role="+ self.__role)
            if error.args[0] == 2:
                print(error.args[1] + error.args[2] + error.args[3])
                logging.debug("Show user role couldn't finish cause : role="+ self.__role)


def db_acces():

    """
    This function allows to check the access to the database.

    PRE : -
    POST : It returns if you have the access to the database or not
    RAISES : -
    """
    try:
        with DataBaseCommand() as connector:
            connector.test_connect.admin.command('ismaster')
            print('La base de données est joignable')
    except ConnectionFailure:
        print("La base de données est injoignable")

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
    def display_result(data2=None, screen=0):
        """
        This function is used to display the result of the commands.

        PRE : -
        POST : It displays the result
        RAISES : -
        """
        if screen == 1:
            com = Command()
            com.get_name(data2.lower())
            choice = com.name
            local = LocalMachineCommand()
            network = NetworkStatCommand()
            role_cmd = RoleManagementCommand(data2)
            stat = UserStatCommand(data2)
            try:
                if choice == 'network':
                    print('LOCAL ADDRESS :')
                    print('IPV4 ADDRESS :', local.get_data(network.get_ipv4_local()), '/', local.get_data(
                        network.get_masque('local')))
                    print('IPV6 ADDRESS :', local.get_data(network.get_ipv6_local()))
                    print('PUBLIC ADDRESS :')
                    print('IPV4 ADDRESS :', local.get_data(network.get_ipv4_public()), '/', local.get_data(
                        network.get_masque('public')))
                    print('PING :')
                    local.get_data(network.get_ping())
                elif choice == 'statusers':
                    return stat.stat()
                elif choice == 'histocommand':
                    stat.histo_com()
                elif choice == 'graphmessages':
                    stat.graph_mess()
                elif choice == 'statspam':
                    return stat.stat_spam()
                elif choice == 'statconnected':
                    stat.stat_co()
                elif choice == 'statchannel':
                    return stat.stat_chan()
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
                    return role_cmd.show_user_role()
                elif choice == 'dbacces':
                    db_acces()
                elif choice == 'help':
                    help_str()
                else:
                    return 'Commande entrée inconnue'
            except IndexError:
                print('Veuillez entrée les arguments nécessaire')

        else:
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
                        print('IPV4 ADDRESS :', local.get_data(network.get_ipv4_local()), '/', local.get_data(
                            network.get_masque('local')))
                        print('IPV6 ADDRESS :', local.get_data(network.get_ipv6_local()))
                        space.get_space()
                        print('PUBLIC ADDRESS :')
                        print('IPV4 ADDRESS :', local.get_data(network.get_ipv4_public()), '/', local.get_data(
                            network.get_masque('public')))
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
                                collection = connector.db["roles"]
                                collection2 = connector.db["users"]
                                list_users = collection.find()
                                list_msg = collection2.find()
                                for users in list_users:
                                    print("user:", users)
                                print()
                                for msg in list_msg:
                                    print('msg:', msg)
                        except Exception as e:
                            print(e)
                    elif choice == 'end':  # On passe le flag à true ça finit la boucle si l'utilisateur tape 'end'
                        print('Merci d\'avoir utilisé le Chabot')
                        flag = True
                    else:
                        print('Entrée Help pour avoir une liste des commandes.')
                except IndexError:
                    print('Veuillez entrée les arguments nécessaire')



if __name__ == "__main__":
    res = Result()
    res.display_result()
