class Terrain:
    """
    Clase terreno que identifica un hexágono del tablero
    """

    id = int
    hasThief = bool
    probability = int
    contactingNodes = []

    def __init__(self, id, contacting_nodes, hasThief):
        pass
