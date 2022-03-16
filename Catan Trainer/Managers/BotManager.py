from Interfaces.BotInterface import BotInterface


class BotManager:
    """
    Clase que se encarga de los bots. De momento solo los carga en la partida, sin embargo cabe la posibilidad de que sea
    el bot manager el que se encargue de darle paso a los bots a hacer sus turnos
    """
    actualPlayer = BotInterface()
    playerOne = BotInterface()
    playerTwo = BotInterface()
    playerThree = BotInterface()
    playerFour = BotInterface()

    def __init__(self):
        self.playerOne = BotInterface()
        self.playerTwo = BotInterface()
        self.playerThree = BotInterface()
        self.playerFour = BotInterface()
        return

    def load_bots(self):
        """
        Carga bots en la partida. Debería de coger 4 scripts de una carpeta, donde todas hereden de BotInterface y
         las introduce en los correspondientes jugadores.
        :return: void
        """
        self.playerOne = BotInterface()
        self.playerTwo = BotInterface()
        self.playerThree = BotInterface()
        self.playerFour = BotInterface()
        print('bot loading')
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
