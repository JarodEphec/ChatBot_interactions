import socket
import subprocess

#tableau avec les mots-clés
mots = ['ipv4', 'ipv6', 'masque']

if __name__ == "__main__":
    def main():
        ip4 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Création du socket IPV4
        ip6 = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM) #Création du socket IPV6

        ip4.connect(("8.8.8.8", 80)) #Connexion à l'adresse 8.8.8.8 de google e on regarde le port 80
        ip6.connect(("2001:4860:4860::8888", 80)) #Connexion à l'adresse 2001:4860:4860::8888 de google et on regarde le port 80

        ip = ip4.getsockname()[0] #Récupération de l'adresse IPV4 dans le socket

        proc = subprocess.Popen('ipconfig', stdout=subprocess.PIPE) #Fonction qui exécuter ipconfig et crée un pipe
        while True: #on parcourt le pipe
            line = proc.stdout.readline()
            if ip.encode() in line: #On retrouve la ligne avec l'adresse ipv4 local
                break
        netmask = proc.stdout.readline().rstrip().split(b':')[-1].replace(b' ', b'').decode() #On retire les caractères et extrait le masque de sous-réseau

        #Affichage des messages de bienvenu
        print('Bienvenu dans le Chatbot')
        print('Vous pouvez tapez des mots-clés pour avori accès à vos données réseaux')
        print('Pour mettre fin à la discussion tapez : fin')
        print('')

        flag = False #On définit un flag pour aider à boucler
        choix = str(input('Choisissez un mot-clé :')).lower() #Input pour entrer les mots-clés

        while flag == False:
            choix = str(input('Choissisez un autre mot-clé :')).lower()
            if choix == 'ipv4':
                print('IPV4 ADDRESS LOCAL :', ip4.getsockname()[0]) #Affichage de l'adresse IPV4

            elif choix == 'masque':
                print('SUBNET MASK :', netmask) #Affichage du masque de sous-réseau
            elif choix == 'ipv6':
                print('IPV6 ADDRESS LOCAL :', ip6.getsockname()[0]) #Affichage de l'adresse IPV6

            elif choix == 'fin': #On passe le flag à true ça finit la boucle si l'utilisateur tape 'fin'
                print('Merci d\'avoir utiliser le Chabot')
                flag = True
main()