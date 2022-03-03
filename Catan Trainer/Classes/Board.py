from Classes.Constants import HarborConstants
from Classes.Utilities import is_even


class Board:
    """
    Clase que representa una instancia del tablero.

    nodes: [{"id": int,
             "adjacent": [int...],
             "harbor": int,
             "roads": [{playerID = id, nodeID = int}...],
             "hasCity": bool,
             "player": int}] Representa los nodos del tablero. Poseen información de los puertos y nodos adyacentes

    terrain: [{"id": int,
               "hasThief": bool,
               "probability": int(2,12),
               "contactingNodes": [int...]}]

              Representa una ficha de terreno del tablero. Poseen información de los nodos con
                 los que hacen contacto, si posee al ladrón actualmente y su probabilidad de salir
    """
    nodes = []  # 0 a 53
    terrain = []  # 0 a 18 | Al recorrer este array para mirar la probabilidad cortar si se han encontrado 2 respuestas

    def __init__(self, nodes=None, terrain=None):
        """
        Cuando se llama al init se establece el valor inicial del tablero antes de que se pongan pueblos y carreteras.
        Aquí se pone el terreno y su probabilidad
        """
        if nodes is None:
            i = 0
            while i < 54:
                self.nodes.append({
                    "id": i,
                    "adjacent": self.__get_adjacent_nodes(i),
                    "harbor": self.__get_harbors(i),
                    "roads": [],
                    "hasCity": False,
                    "player": 0,
                })
                i += 1
        else:
            self.nodes = nodes
        if terrain is None:
            j = 0
            while j < 19:
                probability = self.__get_probability(j)
                if probability != 7:
                    self.terrain.append({
                        "id": j,
                        "hasThief": False,
                        "probability": probability,
                        "contactingNodes": self.__get_contacting_nodes(j),
                    })
                else:
                    self.terrain.append({
                        "id": j,
                        "hasThief": True,
                        "probability": 0,
                        "contactingNodes": self.__get_contacting_nodes(j),
                    })
                j += 1
        else:
            self.terrain = terrain

        ### Código para comprobar que el tablero se inicializa con los adyacentes correctos
        # print('Nodos:')
        # n = 0
        # while n < 54:
        #     print(self.nodes[n]['id'])
        #     print(self.nodes[n]['adjacent'])
        #     print(self.nodes[n]['harbor'])
        #     print('---------------------\n')
        #
        #     n += 1

        ### Código para comprobar que el tablero se inicializa con el terreno correcto
        # print('Terreno:')
        # m = 0
        # while m < 19:
        #     print(self.terrain[m]['id'])
        #     print(self.terrain[m]['probability'])
        #     print(self.terrain[m]['contactingNodes'])
        #     print('#######################\n')
        #
        #     m += 1
        return

    def get_board(self):
        return self.__class__()

    def __get_contacting_nodes(self, terrain_id):
        """
        Indica todos los nodos a los que la casilla terreno es adyacente, para cosas como por ejemplo repartir materiales
        :param terrain_id: La ID de la pieza del terreno actual
        :return: [node_id, node_id, node_id, node_id, node_id, node_id]
        """

        # Si consigues esquina superior izquierda.
        #   Nodos contactos son nodo +1, +2, (+8, +9, +10), (+10, +11, +12), (+11, +12, +13)
        contacting_nodes = []
        starting_node = -999
        bottom_row_sum = -999

        if 0 <= terrain_id < 3:
            bottom_row_sum = 8
            if terrain_id == 0:
                starting_node = 0
            elif terrain_id == 1:
                starting_node = 2
            elif terrain_id == 2:
                starting_node = 4

        elif 3 <= terrain_id < 7:
            bottom_row_sum = 10
            if terrain_id == 3:
                starting_node = 7
            elif terrain_id == 4:
                starting_node = 9
            elif terrain_id == 5:
                starting_node = 11
            elif terrain_id == 6:
                starting_node = 13

        elif 7 <= terrain_id < 12:
            bottom_row_sum = 11
            if terrain_id == 7:
                starting_node = 16
            elif terrain_id == 8:
                starting_node = 18
            elif terrain_id == 9:
                starting_node = 20
            elif terrain_id == 10:
                starting_node = 22
            elif terrain_id == 11:
                starting_node = 24

        elif 12 <= terrain_id < 16:
            bottom_row_sum = 10
            if terrain_id == 12:
                starting_node = 28
            elif terrain_id == 13:
                starting_node = 30
            elif terrain_id == 14:
                starting_node = 32
            elif terrain_id == 15:
                starting_node = 34

        elif 16 <= terrain_id < 19:
            bottom_row_sum = 8
            if terrain_id == 16:
                starting_node = 39
            elif terrain_id == 17:
                starting_node = 41
            elif terrain_id == 18:
                starting_node = 43

        contacting_nodes.append(starting_node)
        contacting_nodes.append(starting_node + 1)
        contacting_nodes.append(starting_node + 2)
        contacting_nodes.append(starting_node + bottom_row_sum)
        contacting_nodes.append(starting_node + bottom_row_sum + 1)
        contacting_nodes.append(starting_node + bottom_row_sum + 2)

        return contacting_nodes

    def __get_probability(self, node_id):
        # Establecer el tablero con las probabilidades por defecto del mapa de ejemplo de Catán
        if node_id == 17:
            return 2
        elif node_id == 8 or node_id == 14:
            return 3
        elif node_id == 3 or node_id == 10:
            return 4
        elif node_id == 5 or node_id == 16:
            return 5
        elif node_id == 4 or node_id == 18:
            return 6
        elif node_id == 7:
            return 7
        elif node_id == 11 or node_id == 12:
            return 8
        elif node_id == 2 or node_id == 14:
            return 9
        elif node_id == 6 or node_id == 13:
            return 10
        elif node_id == 0 or node_id == 9:
            return 11
        elif node_id == 1:
            return 12
        else:
            return 0

    def __get_adjacent_nodes(self, node_id):
        """
        Función que obtiene los nodos adyacentes de manera automática
        :param node_id: Id del nodo del que se quieren las IDs de los nodos adyacentes
        :return: Array(ID)
        """
        adjacent_nodes = []

        if 0 <= node_id < 7:
            if node_id != 0:
                adjacent_nodes.append(node_id - 1)
            if node_id != 6:
                adjacent_nodes.append(node_id + 1)

            if is_even(node_id):
                adjacent_nodes.append(node_id + 8)

        elif 7 <= node_id < 16:
            if node_id != 7:
                adjacent_nodes.append(node_id - 1)
            if node_id != 15:
                adjacent_nodes.append(node_id + 1)

            if is_even(node_id):
                adjacent_nodes.append(node_id - 8)
            else:
                adjacent_nodes.append(node_id + 10)

        elif 16 <= node_id < 27:
            if node_id != 16:
                adjacent_nodes.append(node_id - 1)
            if node_id != 26:
                adjacent_nodes.append(node_id + 1)

            if is_even(node_id):
                adjacent_nodes.append(node_id + 11)
            else:
                adjacent_nodes.append(node_id - 10)

        elif 27 <= node_id < 38:
            if node_id != 27:
                adjacent_nodes.append(node_id - 1)
            if node_id != 37:
                adjacent_nodes.append(node_id + 1)

            if is_even(node_id):
                adjacent_nodes.append(node_id + 10)
            else:
                adjacent_nodes.append(node_id - 11)

        elif 38 <= node_id < 47:
            if node_id != 37:
                adjacent_nodes.append(node_id - 1)
            if node_id != 46:
                adjacent_nodes.append(node_id + 1)

            if is_even(node_id):
                adjacent_nodes.append(node_id - 10)
            else:
                adjacent_nodes.append(node_id + 8)

        elif 47 <= node_id < 54:
            if node_id != 47:
                adjacent_nodes.append(node_id - 1)
            if node_id != 53:
                adjacent_nodes.append(node_id + 1)

            if not is_even(node_id):
                adjacent_nodes.append(node_id - 8)

        return adjacent_nodes

    def __get_harbors(self, node_id):
        if node_id == 0 or node_id == 1:
            return HarborConstants.WOOD
        elif node_id == 3 or node_id == 4:
            return HarborConstants.CEREAL
        elif node_id == 14 or node_id == 15:
            return HarborConstants.CLAY
        elif node_id == 28 or node_id == 38:
            return HarborConstants.MINERAL
        elif node_id == 50 or node_id == 51:
            return HarborConstants.WOOL
        elif (node_id == 7 or node_id == 17 or node_id == 26 or node_id == 37 or
              node_id == 45 or node_id == 46 or node_id == 47 or node_id == 48):
            return HarborConstants.ALL
        else:
            return HarborConstants.NONE

    def build_town(self, player, node=-1):
        """
        Permite construir un pueblo por el jugador especificado en el cruce escrito
        Cambia la variable nodes para colocar un pueblo en ello
        :param player: Número que representa al jugador
        :param node: Número que representa un nodo en el tablero
        :return: {bool, string}. Devuelve si se ha podido o no construir el poblado, y en caso de no el porqué
        """
        if self.nodes[node]['player'] == 0:
            self.nodes[node]['player'] = player
            self.nodes[node]['hasCity'] = False
            return True
        else:
            return False

    def build_city(self, player, node=-1):
        """
        Permite construir una ciudad por el jugador especificado en el cruce escrito
        Cambia la variable nodes para colocar una ciudad en ello
        :param player: Número que representa al jugador
        :param node: Número que representa un nodo en el tablero
        :return: {bool, string}. Envía si se ha podido construir la ciudad y en caso de no haberse podido el porqué
        """

        if self.nodes[node]['player'] == player:
            if self.nodes[node]['hasCity']:
                return {False, 'Ya hay una ciudad tuya en el nodo'}
            self.nodes[node]['player'] = player
            self.nodes[node]['hasCity'] = True
            return {True, ''}
        elif self.nodes[node]['player'] == 0:
            return {True, 'Primero debe construirse un poblado'}
        else:
            return {False, 'Ya posee el nodo otro jugador'}

    def build_road(self, player, starting_node=-1, finishing_node=-1):
        """
        Permite construir una carretera por el jugador especificado en la carretera especificada
        Cambia la variable roads para colocar una carretera del jugador designado en ella
        :param player: Número que representa al jugador
        :param starting_node: Nodo desde el que se inicia la carretera
        :param finishing_node: Nodo al que llega la carretera. Debe ser adyacente
        :return: void
        """

        can_build = False
        for roads in self.nodes[starting_node]['roads']:
            if roads['playerID'] == player:
                can_build = True

        if self.nodes[starting_node]['player'] == player or can_build:
            for roads in self.nodes[starting_node]['roads']:
                if roads['nodeID'] == finishing_node:
                    return {False, 'Ya hay una carretera aquí'}

            self.nodes[starting_node]['roads'].append({'playerID': player, 'nodeID': finishing_node})
            self.nodes[finishing_node]['roads'].append({'playerID': player, 'nodeID': starting_node})
            return {True, ''}
        else:
            return {False,
                    'No puedes hacer una carretera aquí, no hay una carretera o nodo adyacente que te pertenezca'}

    def move_thief(self, terrain=-1):
        """
        Permite mover el ladrón a la casilla de terreno especificada
        Cambia la variable terrain para colocar al ladrón en el terreno correspondiente
        :param terrain: Número que representa un hexágono en el tablero
        :return: void
        """
        for square in self.terrain:
            if square['hasThief']:
                square['hasThief'] = False
                break

        self.terrain[terrain]['hasThief'] = True
        return

    def update_board(self):
        """
        Actualiza visualmente el tablero con todos los cambios habidos desde el último update
        TODO:
        :return: void
        """
        return

# if __name__ == '__main__':
#     print('#############################')
#     Board()
#     print('#############################')
