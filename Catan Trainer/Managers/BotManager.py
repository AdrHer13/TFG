from Interfaces.BotInterface import BotInterface


class BotManager:
    """
    Clase que se encarga de los bots. De momento solo los carga en la partida, sin embargo cabe la posibilidad de que sea
    el bot manager el que se encargue de darle paso a los bots a hacer sus turnos
    """
    actualPlayer = BotInterface()
    playerOne = BotInterface(1)
    playerTwo = BotInterface(2)
    playerThree = BotInterface(3)
    playerFour = BotInterface(4)

    def __init__(self):
        self.playerOne = BotInterface(1)
        self.playerTwo = BotInterface(2)
        self.playerThree = BotInterface(3)
        self.playerFour = BotInterface(4)
        return

    def load_bots(self):
        """
        Carga bots en la partida. Debería de coger 4 scripts de una carpeta, donde todas hereden de BotInterface y
         las introduce en los correspondientes jugadores.
        :return: void
        """
        self.playerOne = BotInterface(1)
        self.playerTwo = BotInterface(2)
        self.playerThree = BotInterface(3)
        self.playerFour = BotInterface(4)
        # print('bot loading')
        return

    def set_actual_player(self, player=0):
        if player == 1:
            self.actualPlayer = self.playerOne
        elif player == 2:
            self.actualPlayer = self.playerTwo
        elif player == 3:
            self.actualPlayer = self.playerThree
        elif player == 4:
            self.actualPlayer = self.playerFour
        else:
            print("EXCEPTION")
            # TODO: throw exception
            return None

    def get_player_from_int(self, player_int=0):
        if player_int == 1:
            return self.playerOne
        elif player_int == 2:
            return self.playerTwo
        elif player_int == 3:
            return self.playerThree
        elif player_int == 4:
            return self.playerFour
        else:
            # TODO: throw exception
            return None

    def get_other_players_except_int(self, player_int=0):
        if player_int == 1:
            return [self.playerTwo, self.playerThree, self.playerFour]
        elif player_int == 2:
            return [self.playerOne, self.playerThree, self.playerFour]
        elif player_int == 3:
            return [self.playerOne, self.playerTwo, self.playerFour]
        elif player_int == 4:
            return [self.playerOne, self.playerTwo, self.playerThree]
        else:
            # TODO: throw exception
            return None
