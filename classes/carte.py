# -*-coding:Utf-8 -*

"""Ce module contient la classe Carte."""

class Carte:

    """Objet de transition entre un fichier et un labyrinthe."""

    def __init__(self, nom, chaine):
        """ Constructeur de la classe"""
        self.nom = nom
        self.chaine = chaine
        self.mapping = self.creer_labyrinthe_depuis_chaine(self.chaine)

    def __repr__(self):
        """Fonction qui definie ce qu'il s'affiche si on print()
        une instance de la classe
        """
        return "<Carte {}>".format(self.nom)

    def creer_labyrinthe_depuis_chaine(self, chaine):
        """Méthode qui crée un mapping du labyrinthe en
        fonction de la chaine de caractère

        Retourne le mapping sous forme de liste
        """
        lignes = chaine.split("\n")
        map_liste = []
        for elt in lignes:
            map_liste.append([c for c in elt])

        return map_liste
