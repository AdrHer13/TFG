from Classes.Board import Board
from Classes.Hand import Hand
from Classes.TradeOffer import TradeOffer
# from Managers.TurnManager import TurnManager
from Managers.GameDirector import GameDirector


class BotInterface:
    """
    Interfaz que implementa a un bot
    """
    gameDirector = GameDirector()
    resources = Hand()
    board = Board()

    def __init__(self, game_director=GameDirector()) -> None:
        super().__init__()
        self.gameDirector = game_director

    def on_trade_offer(self, incoming_trade_offer=TradeOffer()):
        """
        Trigger para cuando llega una oferta
        :param incoming_trade_offer: Oferta de comercio que le llega al bot
        :return: void
        """
        pass

    def on_turn_start(self):
        """
        Trigger para cuando empieza el turno (muy probablemente innecesarios)
        :return: void
        """
        print('Player on turn start')
        self.gameDirector.end_phase()
        return

    def on_turn_end(self):
        """
        Trigger para cuando acaba el turno (muy probablemente innecesarios)
        :return: void
        """
        print('Player on turn end')
        self.gameDirector.end_phase()
        pass

    def on_commerce_phase(self):
        """
        Trigger para cuando empieza la fase de comercio
        :return: void
        """
        print('Player on commerce phase')
        self.gameDirector.end_phase()
        pass

    def on_build_phase(self):
        """
        Trigger para cuando empieza la fase de construcción
        :return: void
        """
        print('Player on build phase')
        self.gameDirector.end_phase()
        pass
