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
        return

    def load_bots(self):
        """
        Carga bots en la partida. Debería de coger 4 scripts de una carpeta, donde todas hereden de BotInterface y
         las introduce en los correspondientes jugadores.
        :return: void
        """
        self.playerOne = BotInterface()
        print('bot loading')
        return

    def set_actual_player(self, player=0):
        if player <= 0:
            # TODO: throw Exception
            return None
        if player == 1:
            self.actualPlayer = self.playerOne
            self.actualPlayerInt = 1
        elif player == 2:
            self.actualPlayer = self.playerTwo
            self.actualPlayerInt = 2
        elif player == 3:
            self.actualPlayer = self.playerThree
            self.actualPlayerInt = 3
        else:
            self.actualPlayer = self.playerFour
            self.actualPlayerInt = 4
        return
