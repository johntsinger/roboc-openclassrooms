# -*-coding:Utf-8 -*

"""Ce fichier contient le code principal du jeu.

Exécutez-le avec Python pour lancer le jeu.

"""

import os
import sys
import time
from classes.carte import Carte
from classes.labyrinthe import Labyrinthe

##################################################
#################### FUNCTIONS ###################
##################################################

def load_map():
    """Cherche le dossier cartes, charge les fichier .txt
    qui contiennent les cartes, les lis et crée l'objet carte
    pour chaque fichier existant puis l'ajoute a la liste

    retourne la liste des cartes
    """
    cartes = []
    for nom_fichier in os.listdir("cartes"):
        if nom_fichier.endswith(".txt"):
            chemin = os.path.join("cartes", nom_fichier)
            nom_carte = nom_fichier[:-3].lower()
            with open(chemin, "r") as fichier:
                contenu = fichier.read()
                cartes.append(Carte(nom_carte, contenu))
    return cartes

def check_save(cartes):
    """Verifie si une sauvegarde existe dans la liste des cartes
    et demande a l'utilisateur de si il veux charger sa sauvegarde

    Retourne l'index de la partie sauvegarder
    """
    index = None
    for carte in cartes:
        if carte.nom == "sauvegarde.":
            text = """Vous n'avez pas terminer votre dernière partie\n
Voulez vous la reprendre ? (O/N) : """
            answer = input(text)
            print("")
            if answer.lower() == "o":
                index = cartes.index(carte)
            elif answer.lower() == "q":
                print("""Vous quitter le jeu
\nFermeture du programme""")
                time.sleep(1)
                sys.exit(0)

    return index

def choose_map(cartes):
    """
    Demande à l'utilisateur de choisir une carte et
    verifie si l'entrée est valide

    retourne le choix de l'utilisateur
    """
    choix = ""
    while choix == "":
        choix = input("Choisisser une carte : ")
        if choix.lower() == "q":
            print("""\nVous quitter le jeu
\nFermeture du programme""")
            time.sleep(1)
            sys.exit(0)
        else:
            try:
                choix = int(choix)
            except ValueError:
                print("\nVeuillez entrer un nombre valide\n")
                choix = ""
                continue
            if choix not in [i+1 for i, carte in enumerate(cartes)]:
                print("\nCette carte n'existe pas")
                choix = ""
            print("")

    return choix - 1 # -1 pour obtenir l'indice dans la liste

def verify_input(labyrinthe):
    """Verifie si l'entrée utilisateur est bien une lettre ou une lettre
    et un chiffre/nombre

    retourne la lettre et le chiffre/nombre
    """
    move = ""
    while move == "":
        move = input("Mouvement : ")
        if len(move) > 1:
            lettre = move[0]
            chiffre = move[1:]
            try:
                chiffre = int(chiffre)
            except ValueError:
                print("")
                print(labyrinthe.chaine)
                print("\nDéplacement inconnu\n\nDéplacement autorisé : <N>, <S>, <E>, <O>\n")
                move = ""
                continue
        else:
            lettre = move
            chiffre = 1
            if not lettre.isalpha():
                print("")
                print(labyrinthe.chaine)
                print("\nDéplacement inconnu\n\nDéplacement autorisé : <N>, <S>, <E>, <O>\n")
                move = ""

    return lettre.lower(), chiffre

def play_again():
    """Demande à l'utilisateur si il veut rejouer ou quitter"""
    replay = input("\nVoulez vous rejouer ?\n\
\nAppuyer sur <Enter> pour relancer ou <Q> pour quitter : ").upper()
    print("")
    if replay.lower() == "q":
        print("""Vous quitter le jeu
\nFermeture du programme""")
        time.sleep(1)
    else:
        main()

def save(chaine):
    """Sauvegarde la partie"""
    with open("cartes/sauvegarde.txt", 'w') as fichier:
        fichier.write(chaine)

def print_commands():
    """Affiche les commandes du labyrinthe"""
    print("""Jeu du labyrinthe :\n
Déplacements : nord = <N>
               sud = <S>
               est = <E>
               ouest = <O>\n
<Q> pour quitter\n""")

def print_maps(cartes):
    """Affiche les cartes existantes en fonction des cartes charger"""
    print("Labyrinthes existants :")
    for i, carte in enumerate(cartes):
        print("  {} - {}".format(i + 1, carte.nom))
    print("")

##################################################
#################### MAIN FUNCTION ###############
##################################################

def main():
    """Fonction d'execution du labyrinthe"""
    print_commands()
    cartes = load_map()
    print_maps(cartes)
    choix = check_save(cartes)
    if not choix:
        choix = choose_map(cartes)

    # Creation du labyrinthe :
    carte = cartes[choix]
    lab = Labyrinthe("X", carte.chaine, carte.mapping, wall="O", door=".", exit="U")
    print(lab)

    # Boucle jusqu'à que l'utilisateur quit ou trouve la sortie :
    play = True
    while play:
        print("")
        lettre, chiffre = verify_input(lab)
        if lettre == 'q' and chiffre == 1:
            print("\nVous quitter la partie")
            save(lab.chaine)
            play = False
        else:
            lab.move_to(lettre, chiffre)
            save(lab.chaine)

            if lab.elt_suppr == 'U':
                print("\nVous avez gagnez !!!")
                play = False
                if os.path.exists("cartes/sauvegarde.txt"):
                    os.remove("cartes/sauvegarde.txt")

    play_again()

if __name__ == '__main__':
    main()
