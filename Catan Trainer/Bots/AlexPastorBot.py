import random

from Classes.Constants import *
from Classes.Materials import Materials
from Classes.TradeOffer import TradeOffer
from Interfaces.BotInterface import BotInterface


class AlexPastorBot(BotInterface):
    """
    Es necesario poner super().nombre_de_funcion() para asegurarse de que coge la función del padre
    """

    def __init__(self, bot_id):
        super().__init__(bot_id)

    def on_turn_start(self):
        # Si tiene una carta de desarrollo la usa
        if len(self.development_cards_hand.check_hand()):
            return self.development_cards_hand.select_card_by_id(self.development_cards_hand.hand[0].id)
        return

    def on_turn_end(self):
        # Si tiene una carta de desarrollo la usa
        if len(self.development_cards_hand.check_hand()):
            return self.development_cards_hand.select_card_by_id(self.development_cards_hand.hand[0].id)
        return



