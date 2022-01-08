#
# Clase que se encarga de dirigir una partida de Catan
#
from Classes.Board import Board
from Managers.TurnManager import TurnManager
from Managers.CommerceManager import CommerceManager
from Managers.BotManager import BotManager


class GameManager:
    lastDiceRoll = 0
    board = Board()
    turnManager = TurnManager()
    commerceManager = CommerceManager()
    botManager = BotManager()

    # init()
    def __init__(self):
        return

    # throw_dice() -> int (2, 12)
    #
    # Función que devuelve un valor entre el 2 y el 12, simulando una tirada de 2d6
    def throw_dice(self):
        return

    # give_resources() -> void
    #
    # Función que entrega materiales a cada uno de los jugadores en función de la tirada de dados
    def give_resources(self):
        return

    ########### Board functions ###################

    # build_town(player, node) -> void
    #
    # Permite construir un pueblo en el nodo seleccionado
    def build_town(self, player, node):
        self.board.build_town(player, node)
        return

    # build_city(player, node) -> void
    #
    # Permite construir una ciudad en el nodo seleccionado
    def build_city(self, player, node):
        self.board.build_city(player, node)
        return

    # build_road(player, road) -> void
    #
    # Permite construir una carretera en el camino seleccionado
    def build_road(self, player, road):
        self.board.build_road(player, road)
        return

    # move_thief(terrain, adjacentPlayer) -> void
    #
    # Permite mover al ladrón a la casilla de terreno seleccionada y en caso de que haya un poblado o ciudad de otro
    # jugador adyacente a dicha casilla permite robarle un material aleatorio de la mano.
    def move_thief(self, terrain, adjacentPlayer):
        self.board.move_thief(terrain)
        # TODO: Crear función que permita robar materiales de la mano a los jugadores
        return
