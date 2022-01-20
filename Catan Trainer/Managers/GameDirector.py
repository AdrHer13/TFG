from Managers.TurnManager import TurnManager
from Managers.BotManager import BotManager

from Managers.GameManager import GameManager


class GameDirector:
    """
    Clase que se encarga de dirigir la partida, empezarla y acabarla
    """
    turn_manager = TurnManager()
    bot_manager = BotManager()
    game_manager = GameManager()

    def __init__(self):
        return

    # Turn #
    def start_turn(self, player=int):
        """
        Esta función permite iniciar el turno
        :param player: número que representa al jugador
        :return: void
        """
        return

    def start_commerce_phase(self, player=int):
        """
        Esta función permite pasar a la fase de comercio
        :param player: número que representa al jugador
        :return: void
        """
        return

    def start_build_phase(self, player=int):
        """
        Esta función permite pasar a la fase de construcción
        :param player: número que representa al jugador
        :return: void
        """
        return

    def end_turn(self, player=int):
        """
        Esta función permite finalizar el turno
        :param player: número que representa al jugador
        :return: void
        """
        return

    # Round #
    def round_start(self):
        """
        Esta función permite comenzar una ronda nueva
        :return:
        """
        return

    def round_end(self):
        """
        Esta función permite acabar una ronda empezada
        :return:
        """
        return

    # Game #
    def game_start(self):
        """
        Esta función permite comenzar una partida nueva
        :return:
        """
        return

    def game_end(self):
        """
        Esta función permite acabar una partida empezada
        :return:
        """
        return
    