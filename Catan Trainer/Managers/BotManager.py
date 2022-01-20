from Interfaces.BotInterface import BotInterface
from Managers.GameDirector import GameDirector


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

    def __init__(self, game_director=GameDirector()):
        self.playerOne = BotInterface(game_director)
        self.playerTwo = BotInterface(game_director)
        self.playerThree = BotInterface(game_director)
        self.playerFour = BotInterface(game_director)
        return

    def load_bots(self):
        """
        Carga bots en la partida
        :return: void
        """
        print('bot loading')
        return

    def set_actual_player(self, player=int):
        if player == 1:
            self.actualPlayer = self.playerOne
        elif player == 2:
            self.actualPlayer = self.playerTwo
        elif player == 3:
            self.actualPlayer = self.playerThree
        else:
            self.actualPlayer = self.playerFour
        return
