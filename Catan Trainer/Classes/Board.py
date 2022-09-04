import random

from Classes.Constants import HarborConstants, TerrainConstants
from Classes.Utilities import is_even


class Board:
    """
    Clase que representa una instancia del tablero.

    nodes: [{"id": int,
             "adjacent": [int...],
             "harbor": int,
             "roads": [{"playerID": id, "nodeID": int}...],
             "hasCity": bool,
             "player": int,
             "contactingTerrain": [int...]}] Representa los nodos del tablero. Poseen información de los puertos y nodos adyacentes

    terrain: [{"id": int,
               "hasThief": bool,
               "probability": int(2,12),
               "terrainType": int,
               "contactingNodes": [int...]}]

              Representa una ficha de terreno del tablero. Poseen información de los nodos con
                 los que hacen contacto, si posee al ladrón actualmente y su probabilidad de salir
    """
    nodes = []  # 0 a 53
    terrain = []  # 0 a 18 | Al recorrer este array para mirar la probabilidad cortar si se han encontrado 2 respuestas

    def __init__(self, nodes=None, terrain=None):
        self.nodes = []
        self.terrain = []
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
                    "player": -1,
                    "contactingTerrain": self.__get_contacting_terrain(i),
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
                        "terrainType": self.__get_terrain_type(j),
                        "contactingNodes": self.__get_contacting_nodes(j),
                    })
                else:
                    self.terrain.append({
                        "id": j,
                        "hasThief": True,
                        "probability": 0,
                        "terrainType": self.__get_terrain_type(j),
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

        # ## Código para comprobar que el tablero se inicializa con el terreno correcto
        # print('Terreno:')
        # m = 0
        # while m < 19:
        # print(self.terrain[m]['id'])
        # print(self.terrain[m]['probability'])
        # print(self.terrain[m]['contactingNodes'])
        # print(self.terrain[m]['terrainType'])
        # print('#######################\n')

        # m += 1
        return

    def get_board(self):
        return self.__class__()

    def __get_contacting_terrain(self, node_id):
        """
        Indica todas las piezas de terreno a los que el nodo es adyacente, para cosas como por ejemplo repartir materiales
        :param node_id: La ID de la pieza del terreno actual
        :return: [terrain_id, terrain_id, terrain_id, terrain_id, terrain_id, terrain_id]
        """

        contacting_terrain = []

        if 0 <= node_id <= 2 or 8 <= node_id <= 10:
            contacting_terrain.append(0)
        if 2 <= node_id <= 4 or 10 <= node_id <= 12:
            contacting_terrain.append(1)
        if 4 <= node_id <= 6 or 12 <= node_id <= 14:
            contacting_terrain.append(2)
        if 7 <= node_id <= 9 or 17 <= node_id <= 19:
            contacting_terrain.append(3)
        if 9 <= node_id <= 11 or 19 <= node_id <= 21:
            contacting_terrain.append(4)
        if 11 <= node_id <= 13 or 21 <= node_id <= 23:
            contacting_terrain.append(5)
        if 13 <= node_id <= 15 or 23 <= node_id <= 25:
            contacting_terrain.append(6)
        if 16 <= node_id <= 18 or 27 <= node_id <= 29:
            contacting_terrain.append(7)
        if 18 <= node_id <= 20 or 29 <= node_id <= 31:
            contacting_terrain.append(8)
        if 20 <= node_id <= 22 or 31 <= node_id <= 33:
            contacting_terrain.append(9)
        if 22 <= node_id <= 24 or 33 <= node_id <= 35:
            contacting_terrain.append(10)
        if 24 <= node_id <= 26 or 35 <= node_id <= 37:
            contacting_terrain.append(11)
        if 28 <= node_id <= 30 or 38 <= node_id <= 40:
            contacting_terrain.append(12)
        if 30 <= node_id <= 32 or 40 <= node_id <= 42:
            contacting_terrain.append(13)
        if 32 <= node_id <= 34 or 42 <= node_id <= 44:
            contacting_terrain.append(14)
        if 34 <= node_id <= 36 or 44 <= node_id <= 46:
            contacting_terrain.append(15)
        if 39 <= node_id <= 41 or 47 <= node_id <= 49:
            contacting_terrain.append(16)
        if 41 <= node_id <= 43 or 49 <= node_id <= 51:
            contacting_terrain.append(17)
        if 43 <= node_id <= 45 or 51 <= node_id <= 53:
            contacting_terrain.append(18)

        return contacting_terrain

    def __get_contacting_nodes(self, terrain_id):
        """
        Indica todos los nodos a los que la casilla terreno es adyacente, para cosas como por ejemplo repartir materiales
        :param terrain_id: La ID de la pieza del terreno actual
        :return: [node_id, node_id, node_id, node_id, node_id, node_id]
        """

        # Si empiezas en la esquina superior izquierda.
        #   Nodos contactos son nodo +1, +2, (+8, +9, +10); +1, +2, (+10, +11, +12); +1, +2, (+11, +12, +13);
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

    def __get_probability(self, terrain_id):
        # Establecer el tablero con las probabilidades por defecto del mapa de ejemplo de Catán
        if terrain_id == 17:
            return 2
        elif terrain_id == 8 or terrain_id == 15:
            return 3
        elif terrain_id == 3 or terrain_id == 10:
            return 4
        elif terrain_id == 5 or terrain_id == 16:
            return 5
        elif terrain_id == 4 or terrain_id == 18:
            return 6
        elif terrain_id == 7:
            return 7
        elif terrain_id == 11 or terrain_id == 12:
            return 8
        elif terrain_id == 2 or terrain_id == 14:
            return 9
        elif terrain_id == 6 or terrain_id == 13:
            return 10
        elif terrain_id == 0 or terrain_id == 9:
            return 11
        elif terrain_id == 1:
            return 12
        else:
            return 0

    def __get_terrain_type(self, terrain_id):
        """
        Establecer el tablero con el tipo de terreno por defecto del mapa de ejemplo de Catán
        :param terrain_id:
        :return:
        """
        if terrain_id == 0 or terrain_id == 8 or terrain_id == 10 or terrain_id == 18:
            return TerrainConstants.WOOD
        elif terrain_id == 1 or terrain_id == 6 or terrain_id == 13 or terrain_id == 14:
            return TerrainConstants.WOOL
        elif terrain_id == 2 or terrain_id == 9 or terrain_id == 11 or terrain_id == 17:
            return TerrainConstants.CEREAL
        elif terrain_id == 3 or terrain_id == 5 or terrain_id == 12:
            return TerrainConstants.CLAY
        elif terrain_id == 4 or terrain_id == 15 or terrain_id == 16:
            return TerrainConstants.MINERAL
        else:
            # En el caso de ser 7 o cualquier ID inexistente le asigna un desierto
            return TerrainConstants.DESERT

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
        if self.nodes[node]['player'] == -1:
            can_build = False
            for roads in self.nodes[node]['roads']:
                if roads['playerID'] == player:
                    can_build = True

            if not self.adyacent_nodes_dont_have_towns(node):
                return {'response': False, 'errorMsg': 'Hay un pueblo o ciudad muy cercano al nodo'}
            if can_build:
                self.nodes[node]['player'] = player
                self.nodes[node]['hasCity'] = False
                return {'response': True, 'errorMsg': ''}
            else:
                return {'response': False,
                        'errorMsg': 'Debes poseer una carretera hasta el nodo para poder construir un pueblo'}
        else:
            return {'response': False, 'errorMsg': 'No se puede construir en un nodo que le pertenece a otro jugador'}

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
                return {'response': False, 'errorMsg': 'Ya hay una ciudad tuya en el nodo'}
            # self.nodes[node]['player'] = player
            self.nodes[node]['hasCity'] = True
            return {'response': True, 'errorMsg': ''}
        elif self.nodes[node]['player'] == -1:
            return {'response': True, 'errorMsg': 'Primero debe construirse un poblado'}
        else:
            return {'response': False, 'errorMsg': 'Ya posee el nodo otro jugador'}

    def build_road(self, player, starting_node=-1, finishing_node=-1):
        """
        Permite construir una carretera por el jugador especificado en la carretera especificada
        Cambia la variable roads para colocar una carretera del jugador designado en ella
        :param player: Número que representa al jugador
        :param starting_node: Nodo desde el que se inicia la carretera
        :param finishing_node: Nodo al que llega la carretera. Debe ser adyacente
        :return: {bool, string}. Envía si se ha podido construir la carretera y en caso de no haberse podido el porqué
        """
        can_build = False
        # Comprueba si ya había una carretera puesta que le pertenezca al jugador
        for road in self.nodes[starting_node]['roads']:
            if road['nodeID'] == finishing_node:
                # Dejamos de mirar si ya hay una carretera hacia el nodo final
                return {'response': False, 'errorMsg': 'Ya hay una carretera aquí'}
            if road['playerID'] == player:
                can_build = True

        for road in self.nodes[finishing_node]['roads']:
            if road['nodeID'] == starting_node:
                # Dejamos de mirar si ya hay una carretera hacia el nodo final
                return {'response': False, 'errorMsg': 'Ya hay una carretera aquí'}
            if road['playerID'] == player:
                can_build = True

        # Si le pertenece el nodo inicial o tiene una carretera, deja construir
        if self.nodes[starting_node]['player'] == player or can_build:
            self.nodes[starting_node]['roads'].append({'playerID': player, 'nodeID': finishing_node})
            self.nodes[finishing_node]['roads'].append({'playerID': player, 'nodeID': starting_node})

            return {'response': True, 'errorMsg': ''}
        else:
            return {'response': False,
                    'errorMsg': 'No puedes hacer una carretera aquí,' +
                                ' no hay una carretera o nodo adyacente que te pertenezca'}

    def move_thief(self, terrain=-1):
        """
        Permite mover el ladrón a la casilla de terreno especificada
        Cambia la variable terrain para colocar al ladrón en el terreno correspondiente
        :param terrain: Número que representa un hexágono en el tablero
        :return: {bool, string}. Envía si se ha podido move al ladrón y en caso de no haberse podido el porqué
        """
        if self.terrain[terrain]['hasThief']:
            self.terrain[terrain]['hasThief'] = False

            rand_terrain = random.randint(0, 18)
            self.terrain[rand_terrain]['hasThief'] = True
            return {'response': False,
                    'errorMsg': 'No se puede mover al ladrón a la misma casilla',
                    'terrainId': rand_terrain}
        else:
            # Quitamos el ladrón del terreno que lo posea
            for square in self.terrain:
                if square['hasThief']:
                    square['hasThief'] = False
                    break

            self.terrain[terrain]['hasThief'] = True
            return {'response': True,
                    'errorMsg': '',
                    'terrainId': terrain}

    # def update_board(self):
    #     """
    #     Actualiza visualmente el tablero con todos los cambios habidos desde el último update
    #     :return: void
    #     """
    #     return

    def adyacent_nodes_dont_have_towns(self, node_id):
        """
        Comprueba si los nodos a una casilla de distancia del node_id tienen pueblo o ciudad
        :param node_id:
        :return:
        """
        for adjacent_id in self.nodes[node_id]['adjacent']:
            if self.nodes[adjacent_id]['player'] != -1:
                return False
        return True

    def is_it_a_coastal_node(self, node_id):
        coastal_nodes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 14, 15, 16, 17, 25, 26, 27, 28, 36, 37, 38, 39, 45, 46, 47, 48, 49,
                         50, 51, 52, 53]
        if node_id in coastal_nodes:
            return True
        else:
            return False

    def valid_town_nodes(self, player_id):
        """
        Devuelve un array de las ids de los nodos válidos donde el jugador puede poner un pueblo. Deberían de no haber IDs repetidas
        :param player_id: int
        :return: [id...]
        """
        valid_nodes = []
        for node in self.nodes:
            # print('foreach node: ')
            # print(node)
            for road in node['roads']:
                if (road['playerID'] == player_id
                        and self.adyacent_nodes_dont_have_towns(node['id'])
                        and node['player'] == -1
                        and node['id'] not in valid_nodes):
                    valid_nodes.append(node['id'])
        print('````````````````````````````')
        print('valid_town_nodes: ')
        print(valid_nodes)
        print('````````````````````````````')
        return valid_nodes

    def valid_city_nodes(self, player_id):
        """
        Devuelve un array de las ids de los nodos válidos para convertir pueblos en ciudades
        :param player_id: int
        :return: [id...]
        """
        valid_nodes = []
        for node in self.nodes:
            if node['player'] == player_id and not node['hasCity']:
                valid_nodes.append(node['id'])
        print('````````````````````````````')
        print('valid_city_nodes: ')
        print(valid_nodes)
        print('````````````````````````````')
        return valid_nodes

    def valid_road_nodes(self, player_id):
        """
        Devuelve un array de diccionarios con los nodos iniciales y finales en los que se puede hacer una carretera
        :param player_id:
        :return: [{'startingNode': int, 'finishingNode': int}, ...]
        """
        valid_nodes = []
        for node in self.nodes:
            for adjacent in node['adjacent']:
                for road in self.nodes[adjacent]['roads']:
                    if road['playerID'] == player_id and road['nodeID'] != node['id'] and (
                            node['player'] == player_id or node['player'] == -1):
                        valid_nodes.append({'startingNode': node['id'], 'finishingNode': adjacent})
        print('````````````````````````````')
        print('valid_road_nodes: ')
        print(valid_nodes)
        print('````````````````````````````')
        return valid_nodes

# if __name__ == '__main__':
#     print('#############################')
#     Board()
#     print('#############################')
