import random

from Classes.Board import Board
from Classes.Hand import Hand
from Classes.TradeOffer import TradeOffer
from Classes.Constants import MaterialConstants


class BotInterface:
    """
    Interfaz que implementa a un bot
    """
    resources = Hand()
    board = Board()
    materialConstants = MaterialConstants()

    def __init__(self) -> None:
        super().__init__()

    # Los triggers son llamados por el GameDirector las veces que sean necesarias hasta que devuelvan null
    #  o el GameDirector le niegue continuar el trigger
    def on_trade_offer(self, incoming_trade_offer=TradeOffer()):
        """
        Trigger para cuando llega una oferta. Devuelve si la acepta, la niega o envía una contraoferta
        :param incoming_trade_offer: Oferta de comercio que le llega al bot
        :return: true, TradeOffer, false, None
        """
        return None

    def on_turn_start(self):
        """
        Trigger para cuando empieza el turno (muy probablemente innecesarios). Termina cuando hace un return
        :return: void, None
        """
        print('Player on turn start')
        return None

    def on_turn_end(self):
        """
        Trigger para cuando acaba el turno (muy probablemente innecesarios). Termina cuando hace un return
        :return: void, None
        """
        print('Player on turn end')
        return None

    def on_commerce_phase(self):
        """
        Trigger para cuando empieza la fase de comercio. Devuelve una oferta
        :return: TradeOffer, None
        """
        print('Player on commerce phase')
        return None

    def on_build_phase(self):
        """
        Trigger para cuando empieza la fase de construcción. Devuelve un string indicando qué quiere construir
        :return: array[string: (town, city, road, card), int], None
        """
        print('Player on build phase')
        return None

    def on_game_start(self, board_instance=Board()):
        """
        Se llama únicamente al inicio de la partida y sirve para colocar 1 pueblo y una carretera adyacente en el mapa
        :return:
        """
        self.board = board_instance

        node_id = random.randint(0, 53)
        possible_roads = self.board.nodes[node_id]['adjacent']

        return node_id, possible_roads[random.randint(0, len(possible_roads) - 1)]
