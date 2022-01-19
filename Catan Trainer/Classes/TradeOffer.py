from Classes.Materials import Materials


class TradeOffer:
    """
    Clase que representa los intercambios entre jugadores.
    """
    gives = Materials()
    receives = Materials()

    def __init__(self, init=True):
        if init:
            pass
