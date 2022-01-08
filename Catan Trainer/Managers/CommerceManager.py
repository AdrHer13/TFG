#
# Clase que se encarga del comercio entre jugadores
#
from Classes.TradeOffer import TradeOffer


class CommerceManager:
    offerReceiver = int
    maxCounterOffers = 2
    maxOfferPropositions = 2

    def __init__(self):
        return

    # trade_with_the_bank(String gives, String receives) -> void
    # TODO: plantear si es mejor mantenerlo como string o sí sería mejor usar objetos. La comprobación se hace en otro
    #       lugar diferente
    # Sustituye 4 del material pasado por 1 del deseado
    def trade_with_the_bank(self, gives=str, receives=str):
        return

    # trade_with_the_bank_with_port(String gives, String receives) -> void
    #
    # Sustituye 3 del material pasado por 1 del deseado
    def trade_with_the_bank_with_port(self, gives=str, receives=str):
        return

    # trade_with_the_bank_with_upgraded_port(String gives, String receives) -> void
    #
    # Sustituye 2 del material pasado por 1 del deseado
    def trade_with_the_bank_with_upgraded_port(self, gives=str, receives=str):
        return

    # trade_with_player(TradeOffer trade_offer) -> void
    #
    # Permite enviar una oferta a todos los jugadores en la mesa. Si alguno acepta se hará el intercambio
    def trade_with_player(self, trade_offer=TradeOffer()):
        return

    # accept_offer() -> void
    #
    # Permite aceptar la oferta actualmente en curso
    def accept_offer(self):
        return

    # deny_offer(TradeOffer counter_offer = null)
    #
    # Permite denegar la oferta actualmente en curso. Si se le pasa un objeto contraoferta permite enviarle una
    #  contraoferta al iniciador del intercambio
    def deny_offer(self, counter_offer=TradeOffer(None)):
        return
