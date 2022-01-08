from Classes.Materials import Materials


#
# Clase que representa los intercambios entre jugadores.
#
class TradeOffer:
    # qué se ofrece
    gives = Materials()
    # qué se recibe
    receives = Materials()

    def __init__(self, init=True):
        if init:
            # Do something

        return
