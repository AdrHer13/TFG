from Classes.Materials import Materials


class TradeOffer:
    """
    Clase que representa los intercambios entre jugadores.
    """
    gives = Materials()
    receives = Materials()

    def __init__(self, gives=Materials(0, 0, 0, 0, 0), receives=Materials(0, 0, 0, 0, 0)):
        self.gives = gives
        self.receives = receives
        return
