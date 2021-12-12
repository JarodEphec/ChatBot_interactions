import socket
import subprocess
from datetime import datetime


#tableau avec les mots-clés
mots = ['up']

def main ():
    class Command:
        def __init__(self):
            self.name = ''
            self.param = list()
            self.time = datetime

        def get_name(self):
            choix = str(input('Choissisez un mot-clé :')).lower()
            com = choix.split()
            self.name = com[0]
            for x in com[1:]:
                self.param.append(x)
            self.time = datetime.now()
            return choix

    class LocalMachineCommand:
        @staticmethod
        def get_data(self):
            return self

    class NetworkStatCommand:
        @staticmethod
        def get_masque(self):  # Fonction qui renvoie le masque de sous-réseau de l'adresse ipv4
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
                if ip.encode() in line:  ##On retrouve la ligne avec l'adresse ipv4 local récupérée avant
                    break
            netmask = proc.stdout.readline().rstrip().split(b':')[-1].replace(b' ',
                                                                              b'').decode()  # On retire les caractères et extrait le masque de sous-réseau
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
            except:
                return 'Pas d\'adresse ipv6'

        def get_ipv4_public(self):  # Fonction qui renvoie l'adresse ipv4 public
            ipv4 = str(socket.gethostbyname(socket.gethostname()))
            return ipv4

        def get_ping(self):
            return print('En cours de construction...')

    class Result:

        def get_space(self):  # Fonction qui fait une ligne d'espace en console
            return print('')

        def display_result(self): #Fonction d'affichage
            space = Result()
            local = LocalMachineCommand()
            network = NetworkStatCommand()
            # Affichage des messages de bienvenu
            print('Bienvenu dans le Chatbot')
            space.get_space()
            print('Vous pouvez tapez des mots-clés pour avoir accès à vos données réseaux')
            print('Pour mettre fin à la discussion tapez : fin')

            flag = False  # On définit un flag pour aider à boucler

            while flag == False:
                com = Command()
                space.get_space()
                choix = com.get_name()
                space.get_space()
                if choix == 'up':
                    print('LOCAL ADDRESS :')
                    print('IPV4 ADDRESS :', local.get_data(network.get_ipv4_local()), '/',  local.get_data(network.get_masque('local'))) # Affichage de l'adresse IPV4 local
                    print('IPV6 ADDRESS :',  local.get_data(network.get_ipv6_local()))  # Affichage de l'adresse IPV6 local
                    space.get_space()
                    print('PUBLIC ADDRESS :')
                    print('IPV4 ADDRESS :',  local.get_data(network.get_ipv4_public()), '/',  local.get_data(network.get_masque('public')))# Affichage de l'adresse IPV4 public
                    space.get_space()
                    print('PING :')
                    local.get_data(network.get_ping())
                    space.get_space()
                elif choix == 'fin':  # On passe le flag à true ça finit la boucle si l'utilisateur tape 'fin'
                    print('Merci d\'avoir utilisé le Chabot')
                    flag = True
                else:
                    print('Choissisez une des commandes suivantes : up')

    res = Result()
    res.display_result()

if __name__ == "__main__":
    main()