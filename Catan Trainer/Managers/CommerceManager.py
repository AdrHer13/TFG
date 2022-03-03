from Classes.TradeOffer import TradeOffer


class CommerceManager:
    """
     Clase que se encarga del comercio entre jugadores
    """
    offerReceiver = int
    maxCounterOffers = 2
    maxOfferPropositions = 2

    def __init__(self):
        return

    def trade_with_the_bank(self, gives=str, receives=str):
        # TODO: plantear si es mejor mantenerlo como string o sí sería mejor usar objetos. La comprobación se hace en
        #  otro lugar diferente
        """
        Sustituye 4 del material pasado por 1 del deseado
        :param gives: qué material quiere cambiar con el puerto
        :param receives: qué material quiere recibir a cambio
        :return: void
        """
        return

    def trade_through_harbor(self, gives=str, receives=str):
        """
        Sustituye 3 del material pasado por 1 del deseado
        :param gives: qué material quiere cambiar con el puerto
        :param receives: qué material quiere recibir a cambio
        :return: void
        """
        return

    def trade_through_special_harbor(self, gives=str, receives=str):
        """
        Sustituye 2 del material pasado por 1 del deseado
        :param gives: qué material quiere cambiar con el puerto
        :param receives: qué material quiere recibir a cambio
        :return: void
        """
        return

    def trade_with_player(self, trade_offer=TradeOffer()):
        """
        Permite enviar una oferta a todos los jugadores en la mesa. Si alguno acepta se hará el intercambio
        :param trade_offer: Oferta de comercio con el jugador, debe incluir qué se entrega y qué se recibe
        :return: void
        """
        return

    def accept_offer(self):
        """
        Permite aceptar la oferta actualmente en curso
        :return: void
        """
        return

    def deny_offer(self, counter_offer=TradeOffer(None)):
        """
        Permite denegar la oferta actualmente en curso. Si se le pasa un objeto contraoferta permite enviarle una
        contraoferta al iniciador del intercambio
        :param counter_offer: contra-oferta de comercio con el jugador, debe incluir qué se entrega y qué se recibe
        :return: void
        """
        return
