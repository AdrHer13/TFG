from Classes.Board import Board
from Classes.Constants import MaterialConstants, DevelopmentCardConstants
from Classes.DevelopmentCards import *
from Classes.Materials import Materials
from Classes.TradeOffer import TradeOffer
from Managers.BotManager import BotManager
from Managers.CommerceManager import CommerceManager
from Managers.TurnManager import TurnManager


class GameManager:
    """
    Clase que representa el game manager, entidad que tiene todas las acciones que pueden hacer los jugadores
    """
    MAX_COMMERCE_DEPTH = 2

    def __init__(self, for_test=False):
        self.last_dice_roll = 0
        self.largest_army = 2
        self.largest_army_player = {}

        self.board = Board()
        self.development_cards_deck = DevelopmentDeck()
        self.development_cards_deck.shuffle_deck()
        self.turn_manager = TurnManager()
        self.commerce_manager = CommerceManager()
        self.bot_manager = BotManager(for_test)
        return

    def reset_game_values(self):
        """
        Reinicia las variables al valor inicial
        :return: None
        """
        self.last_dice_roll = 0
        self.largest_army = 2
        self.largest_army_player = {}

        self.board = Board()
        self.development_cards_deck = DevelopmentDeck()
        self.development_cards_deck.shuffle_deck()
        self.turn_manager = TurnManager()
        self.commerce_manager = CommerceManager()
        self.bot_manager.reset_game_values()
        return

    def throw_dice(self):
        """
        Función que devuelve un valor entre el 2 y el 12, simulando una tirada de 2d6
        :return: integer entre 2 y 12
        """
        first_d6 = random.randint(1, 6)
        second_d6 = random.randint(1, 6)
        # self.last_dice_roll = random.randint(2, 12)
        self.last_dice_roll = first_d6 + second_d6
        # print('throw dice: ' + str(self.last_dice_roll))
        return

    def give_resources(self):
        """
        Función que entrega materiales a cada uno de los jugadores en función de la tirada de dados
        :return: None
        """
        # Por cada pieza de terreno en el tablero
        for terrain in self.board.terrain:
            # Si la probabilidad coincide
            if terrain['probability'] == self.last_dice_roll:
                # Se miran los nodos adyacentes
                for node in terrain['contacting_nodes']:
                    # Si tiene jugador, implica que hay pueblo
                    if self.board.nodes[node]['player'] != -1:
                        player = self.bot_manager.players[self.board.nodes[node]['player']]
                        # Si tiene ciudad se dan 2 en lugar de 1 material

                        if self.board.nodes[node]['has_city']:
                            # print('J' + str(self.board.nodes[node]['player']) + ' | material: ' + str(
                            #     terrain['terrain_type']) + ' | amount: 2')
                            player['player'].hand.add_material(terrain['terrain_type'], 2)
                            # Es posible que la nomenclatura aquí sea un poco confusa, "resources" es
                            # la mano de materiales del BotManager
                            player['resources'].add_material(terrain['terrain_type'], 2)
                        else:
                            # print('J' + str(self.board.nodes[node]['player']) + ' | material: ' + str(
                            #     terrain['terrain_type']) + ' | amount: 1')
                            player['player'].hand.add_material(terrain['terrain_type'], 1)
                            player['resources'].add_material(terrain['terrain_type'], 1)
        return

    def _give_all_resources(self):
        """
        Función que otorga a todos los jugadores 5 de todos los recursos. Usado solo para debugging
        :return: None
        """
        for player in self.bot_manager.players:
            player['resources'].add_material(MaterialConstants.CEREAL, 5)
            player['resources'].add_material(MaterialConstants.MINERAL, 5)
            player['resources'].add_material(MaterialConstants.CLAY, 5)
            player['resources'].add_material(MaterialConstants.WOOD, 5)
            player['resources'].add_material(MaterialConstants.WOOL, 5)
            player['player'].hand = player['resources']

        return

    def send_trade_to_everyone(self, trade_offer=TradeOffer()):
        """
        Permite enviar una oferta a todos los jugadores en la mesa. Si alguno acepta se hará el intercambio
        :param trade_offer: Oferta de comercio con el jugador, debe incluir qué se entrega y qué se recibe
        :return: array [...dict {}]
        """
        # receivers = self.bot_manager.get_other_players_except_int(self.turn_manager.whoseTurnIsIt)
        answer_object = []

        receivers = []
        for index in range(4):
            if index != self.turn_manager.whose_turn_is_it:
                receivers.append(self.bot_manager.players[index])

        # Se aleatorizan el orden en el que se va a recibir la oferta para evitar que J1 tenga ventaja
        current_index, random_index = len(receivers), 0
        while current_index != 0:
            random_index = math.floor(random.random() * current_index)
            current_index -= 1
            (receivers[current_index], receivers[random_index]) = (receivers[random_index], receivers[current_index])

        giver = self.bot_manager.players[self.turn_manager.whose_turn_is_it]
        for receiver in receivers:
            on_tradeoffer_response = []

            count = 1
            while True:
                # Se hace un bucle de contraofertas hasta que se llegue a una decisión de True o False
                if count % 2 == 0:
                    # Giver toma el papel de receiver porque es una contraoferta
                    response_obj = self._on_tradeoffer_response(giver, receiver, count, trade_offer)
                else:
                    response_obj = self._on_tradeoffer_response(receiver, giver, count, trade_offer)

                on_tradeoffer_response.append(response_obj)
                if isinstance(response_obj['response'], dict):
                    count += 1
                else:
                    break

            if on_tradeoffer_response[(len(on_tradeoffer_response) - 1)]['response']:
                if count % 2 == 0:
                    # print('J' + str(self.turn_manager.whose_turn_is_it) + ' ha aceptado')
                    done = self._trade_with_player(trade_offer, giver, receiver)
                else:
                    # print('J' + str(receiver['id']) + ' ha aceptado')
                    done = self._trade_with_player(trade_offer, receiver, giver)

                if done:
                    on_tradeoffer_response[(len(on_tradeoffer_response) - 1)]['completed'] = True
                    answer_object.append(on_tradeoffer_response)
                    return answer_object
                else:
                    on_tradeoffer_response[(len(on_tradeoffer_response) - 1)]['completed'] = False
            else:
                return
                # print('J' + str(receiver['id']) + ' ha negado')
            answer_object.append(on_tradeoffer_response)
        return answer_object

    def _on_tradeoffer_response(self, receiver, giver, count, trade_offer):
        """
        Función llamada cuando llega una oferta de comercio como respuesta a una oferta de comercio
        :param giver: Player()
        :param receiver: Player()
        :param count: Int
        :param trade_offer: TradeOffer()
        :return json_obj: Objeto json al que se le añaden datos para poder exportarlo correctamente
        :return: json_obj {'count': int, 'giver': Player(), 'receiver': Player(),
                             'trade_offer': TradeOffer(), 'response': True/False}
        """
        json_obj = {
            'count': count,
            'trade_offer': trade_offer.__to_object__(),
            'giver': giver['id'],
            'receiver': receiver['id'],
        }

        response = receiver['player'].on_trade_offer()
        if isinstance(response, TradeOffer):
            if count > self.MAX_COMMERCE_DEPTH:
                json_obj['response'] = False

            else:
                # Se pasa de vuelta al bucle para que rote giver y receiver y se vuelva a preguntar por respuesta
                json_obj['response'] = response.__to_object__()

        else:
            json_obj['response'] = response

        return json_obj

    def _trade_with_player(self, trade_offer=None, giver=None, receiver=None):
        """
        Función que hace el intercambio entre dos jugadores.
        :param trade_offer: (TradeOffer()) El intercambio que se va a hacer.
        :param giver: ({BotInterface(), Hand(), int, DevelopmentCardHand()}) El jugador que da materiales.
        :param receiver: ({BotInterface(), Hand(), int, DevelopmentCardHand()}) El jugador que recibe materiales.
        :return: bool
        """
        if trade_offer is None or giver is None or receiver is None:
            return False

        # Si receiver o giver no tiene materiales se le ignora
        if (receiver['resources'].resources.has_this_more_materials(trade_offer.receives) and
                giver['resources'].resources.has_this_more_materials(trade_offer.gives)):

            materials = ['cereal', 'mineral', 'clay', 'wood', 'wool']

            for i in range(len(materials)):
                material_quantity = getattr(trade_offer.giver, materials[i])
                giver['resources'].remove_material(i, material_quantity)  # Se resta lo que giver entrega
                receiver['resources'].add_material(i, material_quantity)  # Se añade lo que receiver recibe del giver

                material_quantity = getattr(trade_offer.receives, materials[i])
                receiver['resources'].remove_material(i, material_quantity)  # Se resta lo que receiver entrega
                giver['resources'].add_material(i, material_quantity)  # Se añade lo que giver recibe del receiver

            giver['player'].hand = giver['resources']
            receiver['player'].hand = receiver['resources']

            return True
        else:
            return False

    ########### Board functions ###################
    def build_town(self, player_id, node):
        """
        Permite construir un pueblo en el nodo seleccionado.
        :param player_id: (int) Número que representa al jugador.
        :param node: (Tree()) Número que representa un nodo en el tablero.
        :return: {bool, string}. Devuelve si se ha podido o no construir el poblado, y en caso negativo, la razón.
        """
        # TODO: quitar getters? Python no los necesita
        player_hand = self.bot_manager.players[player_id]['resources']
        if player_hand.resources.has_this_more_materials('town'):
            build_town_obj = self.board.build_town(self.turn_manager.whose_turn_is_it, node)

            if build_town_obj['response']:
                player_hand.remove_material([
                    MaterialConstants.CEREAL,
                    MaterialConstants.CLAY,
                    MaterialConstants.WOOD,
                    MaterialConstants.WOOL
                ], 1)
                self.bot_manager.players[player_id]['player'].hand = player_hand

            return build_town_obj
        else:
            return {'response': False, 'error_msg': 'Falta de materiales'}

    def build_city(self, player_id, node):
        """
        Permite construir una ciudad en el nodo seleccionado.
        :param player_id: (int) Número que representa al jugador.
        :param node: (Tree()) Número que representa un nodo en el tablero.
        :return: {bool, string}. Devuelve si se ha podido o no construir la ciudad, y en caso negativo, la razón.
        """
        player_hand = self.bot_manager.players[player_id]['resources']
        if player_hand.resources.has_this_more_materials('city'):
            build_city_obj = self.board.build_city(self.turn_manager.whose_turn_is_it, node)

            if build_city_obj['response']:
                player_hand.remove_material(MaterialConstants.CEREAL, 2)
                player_hand.remove_material(MaterialConstants.MINERAL, 3)
                self.bot_manager.players[player_id]['player'].hand = player_hand

            return build_city_obj
        else:
            return {'response': False, 'error_msg': 'Falta de materiales'}

    def build_road(self, player_id, node, road, free=False):
        """
        Permite construir una carretera en el camino seleccionado.
        :param player_id: (int) Número que representa al jugador.
        :param node: (Tree()) Número que representa.
        :param road: (Tree()) Número que representa una carretera en el tablero.
        :param free: (bool) Usado solo para cuando construyes carreteras gratis con una carta de desarrollo.
        :return: {bool, string}. Devuelve si se ha podido o no construir la carretera, y en caso negativo, la razón.
        """
        player_hand = self.bot_manager.players[player_id]['resources']
        if player_hand.resources.has_this_more_materials('road') or free:
            build_road_obj = self.board.build_road(self.turn_manager.whose_turn_is_it, node, road)

            if build_road_obj['response'] and not free:
                player_hand.remove_material([
                    MaterialConstants.CLAY,
                    MaterialConstants.WOOD,
                ], 1)

            return build_road_obj
        else:
            return {'response': False, 'error_msg': 'Falta de materiales'}

    def build_development_card(self, player_id):
        """
        Permite construir una carta de desarrollo.
        :param player_id: (int) Número que representa al jugador.
        :return: {bool, string, string, string}. Devuelve si se ha podido o no construir la carta de desarrollo,
                                                 el ID de la carta, el tipo de carta que es, el efecto de la carta
                                                 y si no se ha podido hacer, la razón.
        """
        card_drawn = self.development_cards_deck.draw_card()
        if card_drawn is not None:

            player_hand = self.bot_manager.players[player_id]['resources']
            if player_hand.resources.has_this_more_materials(Materials(1, 1, 0, 0, 1)):
                player_hand.remove_material(MaterialConstants.CEREAL, 1)
                player_hand.remove_material(MaterialConstants.MINERAL, 1)
                player_hand.remove_material(MaterialConstants.WOOL, 1)

                if card_drawn.get_type() == DevelopmentCardConstants.VICTORY_POINT:
                    self.bot_manager.players[player_id]['hidden_victory_points'] += 1

                self.bot_manager.players[player_id]['development_cards'].add_card(card_drawn)
                self.bot_manager.players[player_id]['player'].development_cards_hand.hand = \
                    self.bot_manager.players[player_id]['development_cards'].hand

                return {'response': True, 'card_id': card_drawn.id, 'card_type': card_drawn.type,
                        'card_effect': card_drawn.effect}
            else:
                return {'response': False, 'error_msg': 'Falta de materiales'}
        else:
            return {'response': False, 'error_msg': 'No hay más cartas que crear'}

    def move_thief(self, terrain, adjacent_player):
        """
        Permite mover al ladrón a la casilla de terreno seleccionada y en caso de que haya un poblado o ciudad de otro
        jugador adyacente a dicha casilla permite robarle un material aleatorio de la mano.
        :param terrain: Número que representa un hexágono en el tablero
        :param adjacent_player: Número de un jugador que esté adyacente al hexágono seleccionado
        :return: void
        """
        move_thief_obj = self.board.move_thief(terrain)
        move_thief_obj['robbed_player'] = -1
        move_thief_obj['stolen_material_id'] = -1
        if move_thief_obj['response']:
            if adjacent_player != -1:
                for node in self.board.terrain[move_thief_obj['terrain_id']]['contacting_nodes']:
                    if self.board.nodes[node]['player'] == adjacent_player:
                        move_thief_obj['stolen_material_id'] = self._steal_from_player(adjacent_player)
                        move_thief_obj['robbed_player'] = adjacent_player
                        break
                move_thief_obj['error_msg'] = \
                    'No se ha podido robar al jugador debido a que no está en un nodo adyacente'
        return move_thief_obj

    def _steal_from_player(self, player):
        """
        Función que permite robar de manera aleatoria un material de la mano de un jugador.
        :param player: Número que representa a un jugador
        :return: void
        """
        player_obj = self.bot_manager.players[player]
        actual_player_obj = self.bot_manager.players[self.bot_manager.get_actual_player()]
        material_array = []

        # TODO: 100% que existe una mejor manera de montar un array con solo los valores que no sean 0
        if player_obj['resources'].get_cereal() > 0:
            material_array.append(MaterialConstants.CEREAL)
        if player_obj['resources'].get_wool() > 0:
            material_array.append(MaterialConstants.WOOL)
        if player_obj['resources'].get_wood() > 0:
            material_array.append(MaterialConstants.WOOD)
        if player_obj['resources'].get_clay() > 0:
            material_array.append(MaterialConstants.CLAY)
        if player_obj['resources'].get_mineral() > 0:
            material_array.append(MaterialConstants.MINERAL)

        if len(material_array):
            material_id = material_array[random.randint(0, (len(material_array) - 1))]
            player_obj['resources'].remove_material(material_id, 1)
            actual_player_obj['resources'].add_material(material_id, 1)

            player_obj['player'].hand = player_obj['resources']
            actual_player_obj['player'].hand = actual_player_obj['resources']
            return material_id
        return None

    def on_game_start_build_towns_and_roads(self, player):
        """
        Función que te permite poner un pueblo y una carretera. Te las pone automáticamente si no pones un nodo válido
        :param player: contador externo que indica a qué jugador le toca
        :return: node_id, road_to
        """

        # TODO: no asumir que los bots van a devolver siempre algo. Comprobar, y si no devuelven nada entonces elegir por ellos
        # Le da a los jugadores 2 intentos de poner bien los pueblos y carreteras. Si no lo hace el GameDirector lo hará por ellos
        for count in range(3):
            if count < 2:
                node_id, road_to = self.bot_manager.players[player]['player'].on_game_start(self.board)

                terrain_ids = self.board.nodes[node_id]['contacting_terrain']
                materials = []
                for ter_id in terrain_ids:
                    materials.append(self.board.terrain[ter_id]['terrain_type'])

                if (self.board.nodes[node_id]['player'] == -1
                        and self.board.adjacent_nodes_dont_have_towns(node_id)
                        and not self.board.is_it_a_coastal_node(node_id)):

                    # print('______________________')
                    # print('NODO: ' + str(node_id))

                    self.board.nodes[node_id]['player'] = self.turn_manager.get_whose_turn_is_it()
                    # print('Materiales del nodo de J' + str(self.board.nodes[node_id]['player']))
                    # print(materials)

                    # Se le dan materiales a la mano del botManager a la de los bots para que sepan cuantos tienen en realidad
                    self.bot_manager.players[player]['resources'].add_material(materials, 1)
                    self.bot_manager.players[player]['player'].hand.add_material(materials, 1)

                    self.bot_manager.players[player]['victory_points'] += 1

                    # Parte carreteras
                    if self.board.nodes[node_id]['player'] == self.turn_manager.get_whose_turn_is_it():
                        response = self.board.build_road(self.turn_manager.get_whose_turn_is_it(), node_id, road_to)
                        if not response['response']:
                            # print(response['error_msg'])
                            return
                        else:
                            # print('J' + str(self.turn_manager.get_whose_turn_is_it()))
                            # print('actual_node_id: ' + str(node_id) + ' | actual_road_to: ' + str(road_to))
                            return node_id, road_to
                    else:
                        # print("el jugador "+ str(self.turn_manager.get_whose_turn_is_it()) +
                        #       " ha intentado poner una carretera en un nodo que no le pertenece: " + str(road_to))
                        return
                else:
                    illegal = True
                    random_node_id = 0
                    while illegal:
                        # random_node_id = random.randint(0, 53)
                        valid_nodes = self.board.valid_starting_nodes()
                        i = random.randint(0, (valid_nodes.__len__() - 1))
                        random_node_id = valid_nodes[i]
                        if (self.board.nodes[random_node_id]['player'] == -1 and
                                self.board.adjacent_nodes_dont_have_towns(random_node_id) and
                                not self.board.is_it_a_coastal_node(random_node_id)):
                            illegal = False
                        else:
                            illegal = True

                    self.board.nodes[random_node_id]['player'] = self.turn_manager.get_whose_turn_is_it()

                    # Se le dan materiales a la mano del botManager a la de los bots para que sepan cuantos tienen en realidad
                    self.bot_manager.players[player]['resources'].add_material(materials, 1)
                    self.bot_manager.players[player]['player'].hand.add_material(materials, 1)

                    self.bot_manager.players[player]['victory_points'] += 1

                    illegal = True
                    while illegal:
                        possible_roads = self.board.nodes[random_node_id]['adjacent']
                        random_road_to = possible_roads[random.randint(0, len(possible_roads) - 1)]

                        response = self.board.build_road(self.turn_manager.get_whose_turn_is_it(), random_node_id,
                                                         random_road_to)
                        if response['response']:
                            # print('J' + str(self.turn_manager.get_whose_turn_is_it()))
                            # print('random_node_id: ' + str(random_node_id) + ' | random_road_to: ' + str(random_road_to))
                            return random_node_id, random_road_to
                        else:
                            illegal = True
                            # print(response['error_msg'])

    def longest_road_calculator(self, node, depth, longest_road_obj, player_id, visited_nodes):
        """
        Función que calcula la carretera más larga a partir de un nodo
        :param node:
        :param depth:
        :param longest_road_obj:
        :param player_id:
        :param visited_nodes:
        :return:
        """
        for road in node['roads']:
            # print('. . . . . . . ')
            # print('Road to: ' + str(road['node_id']))
            if ((road['node_id'] not in visited_nodes) and
                    (road['player_id'] == player_id or player_id == -1) and
                    (road['player_id'] == node['player'] or node['player'] == -1)):
                visited_nodes.append(road['node_id'])
                # print(visited_nodes)
                # print(node)
                if depth > longest_road_obj['longest_road']:
                    longest_road_obj['longest_road'] = depth
                    longest_road_obj['player'] = player_id
                # print('depth: ' + str(depth))
                # print('player: ' + str(player_id))
                longest_road_obj = self.longest_road_calculator(self.board.nodes[road['node_id']], depth + 1,
                                                                longest_road_obj, road['player_id'], visited_nodes)
        return {'longest_road': longest_road_obj['longest_road'], 'player': longest_road_obj['player']}

    def play_development_card(self, player_id, card):
        """
        :param player_id:
        :param card:
        :return:
        """
        # Si la carta que llega existe en la mano del BotManager se elimina y se hace el efecto. Si no, se hace un return nulo
        # Si la carta es un punto de victoria no se borra de la mano
        # Después se iguala la mano del jugador a la del BotManager para evitar trampas.

        card_obj = {}
        # print('SE JUEGA CARTA DE DESARROLLO')
        # print('CARTA QUE LLEGA: ')
        # print(card)
        # print('CARTAS EN MANO: ')

        # print('player hand checkhand()')
        # print(self.bot_manager.players[player_id]['player'].development_cards_hand.check_hand())
        # print('botmanager hand checkhand()')
        # print(self.bot_manager.players[player_id]['development_cards'].check_hand())

        # self.check_player_hands()

        if card.__to_object__() in self.bot_manager.players[player_id]['development_cards'].check_hand():
            if card.type != DevelopmentCardConstants.VICTORY_POINT:
                # print('BORRAR CARTA')
                self.bot_manager.players[player_id]['development_cards'].delete_card(card.id)

                self.bot_manager.players[player_id]['player'].development_cards_hand.hand = \
                    self.bot_manager.players[player_id]['development_cards'].hand
                return

        else:
            self.bot_manager.players[player_id]['player'].development_cards_hand.hand = \
                self.bot_manager.players[player_id]['development_cards'].hand
            # print('HACEN TRAMPAS')

            card_obj['played_card'] = 'none'
            card_obj['reason'] = 'Trying to use cards they don\'t have'

            return card_obj

        if card.type == DevelopmentCardConstants.KNIGHT:
            # se le suma un nuevo caballero al jugador y se le pide mover al ladrón
            # print('SE JUEGA CABALLERO')
            self.bot_manager.players[player_id]['knights'] += 1
            # print('CANTIDAD CABALLEROS: ' + str(self.bot_manager.players[player_id]['knights']))

            if self.bot_manager.players[player_id]['knights'] > self.largest_army:
                if self.largest_army_player == {}:
                    # Definimos el nuevo poseedor con el ejército más grande
                    self.largest_army_player = self.bot_manager.players[player_id]
                    self.largest_army_player['largest_army'] = 1
                    self.largest_army_player['victory_points'] += 2
                else:
                    # Le quitamos los beneficios al anterior poseedor del ejército grande
                    self.largest_army_player['largest_army'] = 0
                    self.largest_army_player['victory_points'] -= 2

                    # Definimos el nuevo poseedor con el ejército más grande
                    self.largest_army_player = self.bot_manager.players[player_id]
                    self.largest_army_player['largest_army'] = 1
                    self.largest_army_player['victory_points'] += 2

            for terrain in self.board.terrain:
                if terrain['has_thief']:
                    return
                    # print('DESDE: ' + str(terrain['id']))
            on_moving_thief = self.bot_manager.players[player_id]['player'].on_moving_thief()
            move_thief_obj = self.move_thief(on_moving_thief['terrain'], on_moving_thief['player'])
            # print('HASTA: ' + str(move_thief_obj['terrain_id']))
            # print('ROBA A: P' + str(move_thief_obj['robbed_player']))
            # se pasan los cambios al objeto
            card_obj['played_card'] = 'knight'
            card_obj['total_knights'] = self.bot_manager.players[player_id]['knights']
            card_obj['past_thief_terrain'] = move_thief_obj['last_thief_terrain']
            card_obj['thief_terrain'] = move_thief_obj['terrain_id']
            card_obj['robbed_player'] = move_thief_obj['robbed_player']
            card_obj['stolen_material_id'] = move_thief_obj['stolen_material_id']

            return card_obj
        elif card.type == DevelopmentCardConstants.VICTORY_POINT:
            # Si tienen suficientes puntos de victoria para ganar. Ganan automáticamente, si no, no pasa nada

            # print('SE JUEGA PUNTOS DE VICTORIA')
            if (self.bot_manager.players[player_id]['victory_points'] +
               self.bot_manager.players[player_id]['hidden_victory_points']) >= 10:
                # print('SUPERAN 10')

                card_obj['played_card'] = 'victory_point'
                self.bot_manager.players[player_id]['victory_points'] = 10
            else:
                # print('NO SUPERAN 10')
                card_obj['played_card'] = 'failed_victory_point'

            return card_obj
        elif card.type == DevelopmentCardConstants.PROGRESS_CARD:
            # print('SE JUEGA CARTA DE PROGRESO:')

            if card.effect == DevelopmentCardConstants.MONOPOLY_EFFECT:
                # print('  -  MONOPOLIO')
                # Elige material
                material_chosen = self.bot_manager.players[player_id]['player'].on_monopoly_card_use()
                material_sum = 0
                # print('ELIGE MATERIAL: ' + str(material_chosen))

                if material_chosen is None:
                    material_chosen = random.randint(0, 4)

                # for i in range(4):
                # print('PRE Hand_P' + str(i))
                # print(self.bot_manager.players[i]['resources'].resources.__to_object__())
                # print('    -    -    -    -    -    -    -    -    -    -    -    -')
                # Se elimina el material de la mano de todos los jugadores
                for player in self.bot_manager.players:
                    material_sum += player['resources'].get_from_id(material_chosen)
                    player['resources'].remove_material(material_chosen,
                                                        player['resources'].get_from_id(material_chosen))
                    player['player'].hand = player['resources']

                # Se le dan todos los materiales eliminados al que usó la carta
                self.bot_manager.players[player_id]['resources'].add_material(material_chosen, material_sum)
                self.bot_manager.players[player_id]['player'].hand = self.bot_manager.players[player_id]['resources']

                # for i in range(4):
                # print('POST Hand_P' + str(i))
                # print(self.bot_manager.players[i]['resources'].resources.__to_object__())

                # Se añade al objeto el material, la suma, y las nuevas manos tras la resta de materiales
                card_obj['played_card'] = 'monopoly'
                card_obj['material_chosen'] = material_chosen
                card_obj['material_sum'] = material_sum
                for i in range(4):
                    card_obj['hand_P' + str(i)] = self.bot_manager.players[i]['resources'].resources.__to_object__()

                return card_obj

            elif card.effect == DevelopmentCardConstants.ROAD_BUILDING_EFFECT:
                # print('  -  CONSTRUCCIÓN CARRETERAS')

                # Se piden en qué puntos quieren construir carreteras
                road_nodes = self.bot_manager.players[player_id]['player'].on_road_building_card_use()
                # print('NODOS ELEGIDOS: ')
                # print(road_nodes)
                card_obj['played_card'] = 'road_building'

                # Si hay al menos una carretera
                if road_nodes is not None:
                    built = {'response': False}
                    # Si existe una segunda carretera
                    if road_nodes['node_id_2'] is not None:
                        built_2 = {'response': False}
                    else:
                        built_2 = {'response': True}

                    # Mientras no estén construidas las carreteras se vuelve a intentar
                    while not built['response'] and not built_2['response']:
                        # Si ya está construida se ignora
                        if not built['response']:
                            built = self.build_road(player_id, road_nodes['node_id'], road_nodes['road_to'], free=True)
                        if not built_2['response']:
                            built_2 = self.build_road(player_id, road_nodes['node_id_2'], road_nodes['road_to_2'],
                                                      free=True)

                        if isinstance(built, dict):
                            if built['response']:
                                card_obj['valid_road_1'] = True
                            else:
                                card_obj['valid_road_1'] = False

                                # Si no se ha podido construir se cambia de carretera a una aleatoria posible
                                valid_nodes = self.board.valid_road_nodes(player_id)
                                if len(valid_nodes):
                                    road_node = random.randint(0, len(valid_nodes) - 1)
                                    road_nodes['node_id'] = valid_nodes[road_node]['starting_node']
                                    road_nodes['road_to'] = valid_nodes[road_node]['finishing_node']
                                else:
                                    # Si no hay más carreteras posibles se rompe el bucle
                                    card_obj['error_msg'] = 'No hay más nodos válidos para construir una carretera'
                                    break
                        if isinstance(built_2, dict):
                            if built['response']:
                                card_obj['valid_road_2'] = True
                            else:
                                card_obj['valid_road_2'] = False

                                valid_nodes = self.board.valid_road_nodes(player_id)
                                if len(valid_nodes):
                                    road_node = random.randint(0, len(valid_nodes) - 1)
                                    road_nodes['node_id_2'] = valid_nodes[road_node]['starting_node']
                                    road_nodes['road_to_2'] = valid_nodes[road_node]['finishing_node']
                                else:
                                    card_obj['error_msg'] = 'No hay más nodos válidos para construir una carretera'
                                    break

                    # print('    -    -    -    -    -    -    -    -    -    -    ')
                    # print('NODOS COLOCADOS:')
                    # print(road_nodes)
                    # Después del bucle ponemos donde se han construido las carreteras y devolvemos el objeto
                    card_obj['roads'] = road_nodes
                    return card_obj
                else:
                    # Si el objeto carreteras es None implica que no hay carreteras construidas
                    card_obj['roads'] = None
                    return card_obj

            elif card.effect == DevelopmentCardConstants.YEAR_OF_PLENTY_EFFECT:
                # print('  -  AÑO DE LA ABUNDANCIA')
                card_obj['played_card'] = 'year_of_plenty'

                # Eligen 2 materiales (puede ser el mismo 2 veces)
                materials_selected = self.bot_manager.players[player_id]['player'].on_year_of_plenty_card_use()
                card_obj['materials_selected'] = materials_selected
                # print('MATERIALES ELEGIDOS:')
                # print(materials_selected)

                if materials_selected is None:
                    material, material2 = random.randint(0, 4), random.randint(0, 4)
                    materials_selected = {'material': material, 'material_2': material2}

                # print('MANO PRE')
                # print(self.bot_manager.players[player_id]['resources'])
                # Obtienen una carta de ese material elegido
                self.bot_manager.players[player_id]['resources'].add_material(materials_selected['material'], 1)
                self.bot_manager.players[player_id]['resources'].add_material(materials_selected['material_2'], 1)

                # Se actualiza la mano
                self.bot_manager.players[player_id]['player'].hand = self.bot_manager.players[player_id]['resources']

                # print('    -    -    -    -    -    -    -    -    -    -    ')
                # print('MANO POST')
                # print(self.bot_manager.players[player_id]['player'].hand)

                card_obj['hand_P' + str(player_id)] = self.bot_manager.players[player_id][
                    'resources'].resources.__to_object__()
                return card_obj
            return card_obj
        return card_obj

    def check_player_hands(self):
        # print('.  -  .  -  .  -  .  -  .  -  .  -  .  -  .')
        # print('CHECK HANDS')
        # print('Bot Manager: ')
        for i in range(4):
            print('P' + str(i + 1))
            print(self.bot_manager.players[i]['development_cards'].check_hand())
            # print(self.bot_manager.players[i]['development_cards'])

        print('Players: ')
        for i in range(4):
            print('P' + str(i + 1))
            print(self.bot_manager.players[i]['player'].development_cards_hand.check_hand())
            # print(self.bot_manager.players[i]['player'].development_cards_hand)

        print('.  -  .  -  .  -  .  -  .  -  .  -  .  -  .')
