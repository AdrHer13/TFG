from Classes.Materials import Materials


#
# Clase que representa los intercambios entre jugadores.
#
class TradeOffer:
    gives = Materials()
    receives = Materials()

    def __init__(self, init=True):
        if init:
            pass
