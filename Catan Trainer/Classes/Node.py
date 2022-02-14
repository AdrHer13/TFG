from Classes.Constants import HarborConstants


class Node:
    """
    Clase nodo que define una conexión entre carreteras (un vértice de cada hexágono)
    """
    id = int
    adjacent = []
    builtRoads = []  # road()
    harbor = HarborConstants.NONE
    roadTo = []  # debe ser el ID de un nodo adyacente
    hasTown = bool
    hasCity = bool
    playerWhoOwnsIt = int

    # TODO: Plantear el diseño de la clase
    def __init__(self, id, adjacent_nodes, harbor=HarborConstants.NONE):
        pass
