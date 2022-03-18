from Classes.TradeOffer import TradeOffer
from Interfaces.BotInterface import BotInterface


class CommerceManager:
    """
     Clase que se encarga del comercio entre jugadores
    """
    offerReceiver = int
    maxCounterOffers = 2
    maxOfferPropositions = 2

    def __init__(self):
        return

    def trade_without_harbor(self, player, gives, receives):
        """
        Sustituye 4 del material pasado por 1 del deseado
        :param player: BotInterface()
        :param gives: ID del material quiere cambiar con el puerto
        :param receives: ID del material quiere recibir a cambio
        :return: bool | Indica si se ha completado el trato
        """
        player_hand = player.hand
        if player_hand.get_from_id(gives) >= 4:
            player_hand.remove_material(gives, 4)
            player_hand.add_material(receives, 1)
            return player_hand
        else:
            return False

    def trade_through_harbor(self, player, gives, receives):
        """
        Sustituye 3 del material pasado por 1 del deseado
        :param player: BotInterface()
        :param gives: ID del material quiere cambiar con el puerto
        :param receives: ID del material quiere recibir a cambio
        :return: bool | Indica si se ha completado el trato
        """
        player_hand = player.hand.get_resources()
        if player_hand.get_from_id(gives) >= 3:
            player_hand.remove_material(gives, 3)
            player_hand.add_material(receives, 1)
            return True
        else:
            return False

    def trade_through_special_harbor(self, player, gives, receives):
        """
        Sustituye 2 del material pasado por 1 del deseado
        :param player: BotInterface()
        :param gives: ID del material quiere cambiar con el puerto
        :param receives: ID del material quiere recibir a cambio
        :return: bool | Indica si se ha completado el trato
        """
        player_hand = player.hand.get_resources()
        if player_hand.get_from_id(gives) >= 2:
            player_hand.remove_material(gives, 2)
            player_hand.add_material(receives, 1)
            return True
        else:
            return False

    # def trade_with_player(self, trade_offer=TradeOffer(), sender=-1):
    #     """
    #     Permite enviar una oferta a todos los jugadores en la mesa. Si alguno acepta se hará el intercambio
    #     :param trade_offer: Oferta de comercio con el jugador, debe incluir qué se entrega y qué se recibe
    #     :param sender: La única persona a la que no hay que enviar la oferta
    #     :return: void
    #     """
    #     # TODO: Comprobar que alguien acepta la oferta tiene la posibilidad de aceptarla de verdad. Es decir, tiene
    #     #       los materiales necesarios
    #
    #     return

    # def accept_offer(self):
    #     """
    #     Permite aceptar la oferta actualmente en curso
    #     :return: void
    #     """
    #     return
    #
    # def deny_offer(self, counter_offer=TradeOffer(None)):
    #     """
    #     Permite denegar la oferta actualmente en curso. Si se le pasa un objeto contraoferta permite enviarle una
    #     contraoferta al iniciador del intercambio
    #     :param counter_offer: contra-oferta de comercio con el jugador, debe incluir qué se entrega y qué se recibe
    #     :return: void
    #     """
    #     return
