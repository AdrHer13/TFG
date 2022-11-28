from Classes.TradeOffer import TradeOffer
from Interfaces.BotInterface import BotInterface


class AdrianHerasBot(BotInterface):
    """
    Es necesario poner super().nombre_de_funcion() para asegurarse de que coge la función del padre
    """
    def __init__(self, bot_id):
        super().__init__(bot_id)
        pass

    def on_trade_offer(self, incoming_trade_offer=TradeOffer()):
        """
        Hay que tener en cuenta que gives se refiere a los materiales que da el jugador que hace la oferta, luego en este caso es lo que recibe
        :param incoming_trade_offer:
        :return:
        """
        if incoming_trade_offer.gives.has_this_more_materials(incoming_trade_offer.receives):
            return True
        else:
            return False
        # return super().on_trade_offer(incoming_trade_offer)

    def on_turn_start(self):
        return None
        # return super().on_turn_start()

    def on_having_more_than_7_materials(self):
        self.hand.resources.__to_object__()
        self.hand.remove_material()

        return super().on_having_more_than_7_materials()

    def on_moving_thief(self):
        return super().on_moving_thief()

    def on_turn_end(self):
        return super().on_turn_end()

    def on_commerce_phase(self):
        return super().on_commerce_phase()

    def on_build_phase(self, **kwargs):
        return super().on_build_phase(kwargs)

    def on_game_start(self, **kwargs):
        return super().on_game_start(kwargs)

    def on_monopoly_card_use(self):
        return super().on_monopoly_card_use()

    def on_road_building_card_use(self):
        return super().on_road_building_card_use()

    def on_year_of_plenty_card_use(self):
        return super().on_year_of_plenty_card_use()
