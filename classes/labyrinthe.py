# -*-coding:Utf-8 -*

"""Ce module contient la classe Labyrinthe."""

class Labyrinthe:

    """Classe représentant un labyrinthe."""

    def __init__(self, robot, chaine, mapping, **obstacles):
        """Constructeur de la classe"""
        self.robot = robot
        self.grille = obstacles
        self.chaine = chaine
        self.labyrinthe_map = mapping
        self.position = self.position_robot()
        self.moves = {"n": self.north,
                      "s": self.south,
                      "e": self.east,
                      "o": self.west}
        self.elt_suppr = " "

    def __repr__(self):
        """Fonction qui definie ce qu'il s'affiche si on print()
        une instance de la classe
        """
        return self.chaine

    def modify_chaine(self, mapping):
        """Modifie la chaine en fonction du mapping"""
        chaine = ""
        for liste in mapping:
            for elt in liste:
                chaine += elt
            chaine += "\n"
        if chaine.endswith("\n"):
            chaine = chaine[:-1]

        self.chaine = chaine

    def position_robot(self):
        """Cherche la position du robot dans le mapping

        Retourne les index de la position du robot sous forme de liste
        """
        robot = self.robot
        liste = self.labyrinthe_map
        position = []
        for elt in liste:
            if robot in elt:
                position.append(liste.index(elt))
                position.append(elt.index(robot))

        return position

    def move_to(self, lettre, chiffre):
        """Verifie si la lettre est dans le dictionaire self.moves
        Execute move() en foction du nombre de fois que l'utilisateur
        a demandé le deplacement et affiche le labyrinthe a chaque déplacement
        Stop l'execution si move() renvoi une erreur
        """
        position1 = self.position
        number = 0
        if lettre in self.moves.keys():
            for _ in range(chiffre):
                erreur = self.move(lettre)
                position2 = self.position
                if erreur:
                    if position1 == position2:
                        print("")
                        print(self.chaine)
                        print("\nvous ne pouvez pas aller par là !")
                    else:
                        print("\nvous rencontrer un mur après {} déplacements, \
vous ne pouvez pas aller plus loin".format(number))
                    break
                else:
                    print("")
                    print(self.chaine)
                    number += 1
                    if self.elt_suppr == self.grille["exit"]:
                        break
        else:
            print("")
            print(self.chaine)
            print("\nDéplacement inconnu\n\nDéplacement autorisé : <N>, <S>, <E>, <O>")

    def move(self, lettre):
        """Verifie si le robot ne rencontre pas de mur
        Déplace le robot dans le mapping et modify la chaine
        en fonction du mapping

        Retourne 1 si le robot rencontre un mur sinon retourne 0
        """
        position = self.position
        sens = self.moves[lettre](position)
        erreur = 0
        if self.labyrinthe_map[sens[0]][sens[1]] != self.grille["wall"]:
            self.labyrinthe_map[position[0]][position[1]] = self.elt_suppr
            self.elt_suppr = self.labyrinthe_map[sens[0]][sens[1]]
            self.labyrinthe_map[sens[0]][sens[1]] = self.robot
            self.position = sens
            self.modify_chaine(self.labyrinthe_map)
        else:
            erreur = 1

        return erreur

    def north(self, pos):
        """Méthode qui renvoie une liste des index lors d'un
        déplacement vers le nord en fonction de la position du robot
        """
        return [pos[0]-1, pos[1]]

    def south(self, pos):
        """Méthode qui renvoie une liste des index lors d'un
        déplacement vers le sud en fonction de la position du robot
        """
        return [pos[0]+1, pos[1]]

    def east(self, pos):
        """Méthode qui renvoie une liste des index lors d'un
        déplacement vers l'est en fonction de la position du robot
        """
        return [pos[0], pos[1]+1]

    def west(self, pos):
        """Méthode qui renvoie une liste des index lors d'un
        déplacement vers l'ouest en fonction de la position du robot
        """
        return [pos[0], pos[1]-1]
