from Classes.Node import Node


class Board:
    """
    Clase que representa una instancia del tablero.

    nodes: [Node(), Node()...] Representa los nodos del tablero. Poseen información de los puertos y nodos adyacentes
    terrain: [Terrain(), Terrain()...] Representa una ficha de terreno del tablero. Poseen información de los nodos con
                                       los que hacen contacto, si posee al ladrón actualmente y su probabilidad de salir
    """
    nodes = []  # 0 a 53
    terrain = []  # 0 a 19  # Al recorrer este array para mirar la probabilidad cortar si se han encontrado 2 respuestas

    def __init__(self):
        """
        Cuando se llama al init se establece el valor inicial del tablero antes de que se pongan pueblos y carreteras.
        Aquí se pone el terreno y su probabilidad
        """
        i = 0
        while i < 54:
            self.nodes.append(Node(id=i, adjacent_nodes=[]))
            i += 1

        return

    # def build_town(self, player, node):
    #     """
    #     Permite construir un pueblo por el jugador especificado en el cruce escrito
    #     Cambia la variable nodes para colocar un pueblo en ello
    #     :param player: Número que representa al jugador
    #     :param node: Número que representa un nodo en el tablero
    #     :return: void
    #     """
    #     return
    #
    # def build_city(self, player, node):
    #     """
    #     Permite construir una ciudad por el jugador especificado en el cruce escrito
    #     Cambia la variable nodes para colocar una ciudad en ello
    #     :param player: Número que representa al jugador
    #     :param node: Número que representa un nodo en el tablero
    #     :return: void
    #     """
    #     return
    #
    # def build_road(self, player, road):
    #     """
    #     Permite construir una carretera por el jugador especificado en la carretera especificada
    #     Cambia la variable roads para colocar una carretera del jugador designado en ella
    #     :param player: Número que representa al jugador
    #     :param road: Número que representa una carretera en el tablero
    #     :return: void
    #     """
    #     return
    #
    # def move_thief(self, terrain):
    #     """
    #     Permite mover el ladrón a la casilla de terreno especificada
    #     Cambia la variable terrain para colocar al ladrón en el terreno correspondiente
    #     :param terrain: Número que representa un hexágono en el tablero
    #     :return: void
    #     """
    #     return

    def update_board(self):
        """
        Actualiza visualmente el tablero con todos los cambios habidos desde el último update
        :return: void
        """
        return
