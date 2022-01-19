#
# Clase que se encarga de dirigir una partida de Catan
#
from Classes.Board import Board
from Managers.TurnManager import TurnManager
from Managers.CommerceManager import CommerceManager
from Managers.BotManager import BotManager


class GameManager:
    """
    Clase que representa el game manager, entidad que tiene todas las acciones que pueden hacer los jugadores
    """
    lastDiceRoll = 0
    board = Board()
    turnManager = TurnManager()
    commerceManager = CommerceManager()
    botManager = BotManager()

    def __init__(self):
        return

    def throw_dice(self):
        """
        Función que devuelve un valor entre el 2 y el 12, simulando una tirada de 2d6
        :return: integer entre 2 y 12
        """
        return

    def give_resources(self):
        """
        Función que entrega materiales a cada uno de los jugadores en función de la tirada de dados
        :return: void
        """
        return

    ########### Board functions ###################
    def build_town(self, player, node):
        """
        Permite construir un pueblo en el nodo seleccionado
        :param player: Número que representa al jugador
        :param node: Número que representa un nodo en el tablero
        :return: void
        """
        self.board.build_town(player, node)
        return

    def build_city(self, player, node):
        """
        Permite construir una ciudad en el nodo seleccionado
        :param player: Número que representa al jugador
        :param node: Número que representa un nodo en el tablero
        :return: void
        """
        self.board.build_city(player, node)
        return

    def build_road(self, player, road):
        """
        Permite construir una carretera en el camino seleccionado
        :param player: Número que representa al jugador
        :param road: Número que representa una carretera en el tablero
        :return: void
        """
        self.board.build_road(player, road)
        return

    def move_thief(self, terrain, adjacentPlayer):
        """
        Permite mover al ladrón a la casilla de terreno seleccionada y en caso de que haya un poblado o ciudad de otro
        jugador adyacente a dicha casilla permite robarle un material aleatorio de la mano.
        :param terrain: Número que representa un hexágono en el tablero
        :param adjacentPlayer: Número de un jugador que esté adyacente al hexágono seleccionado
        :return: void
        """
        self.board.move_thief(terrain)
        self.__steal_from_player(adjacentPlayer)
        return

    def __steal_from_player(self, player):
        """
        Función que permite robar de manera aleatoria un material de la mano de un jugador.
        :param player: Número que representa a un jugador
        :return: void
        """
        pass
