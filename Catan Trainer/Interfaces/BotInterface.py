from Classes.Hand import Hand
from Classes.TradeOffer import TradeOffer


class BotInterface:
    """
    Interfaz que implementa a un bot
    """
    resources = Hand()

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
        pass

    def on_turn_end(self):
        """
        Trigger para cuando acaba el turno (muy probablemente innecesarios)
        :return: void
        """
        pass

    def on_commerce_phase(self):
        """
        Trigger para cuando empieza la fase de comercio
        :return: void
        """
        pass

    def on_build_phase(self):
        """
        Trigger para cuando empieza la fase de construcción
        :return: void
        """
        pass
