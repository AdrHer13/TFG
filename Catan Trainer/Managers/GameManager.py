from Classes.Board import Board
from Classes.Constants import MaterialConstants, DevelopmentCardConstants
from Classes.DevelopmentCards import *
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
                            player['player'].hand.add_material(terrain['terrain_type'], 2)
                            # Es posible que la nomenclatura aquí sea un poco confusa, "resources" es
                            # la mano de materiales del BotManager
                            player['resources'].add_material(terrain['terrain_type'], 2)
                        else:
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
        answer_object = []

        receivers = self.bot_manager.players.copy()
        giver = receivers.pop(self.turn_manager.whose_turn_is_it)

        # Se aleatorizan el orden en el que se va a recibir la oferta para evitar que J1 tenga ventaja
        random.shuffle(receivers)

        for receiver in receivers:
            on_tradeoffer_response = []

            count = 1
            offer = True
            while offer:
                # Se hace un bucle de contraofertas hasta que se llegue a una decisión de True o False
                if count % 2 == 0:
                    # Giver toma el papel de receiver porque es una contraoferta
                    response_obj = self._on_tradeoffer_response(giver, receiver, count, trade_offer)
                else:
                    response_obj = self._on_tradeoffer_response(receiver, giver, count, trade_offer)

                if isinstance(response_obj["response"], TradeOffer):
                    trade_offer = response_obj['response']
                    response_obj['response'] = True
                    on_tradeoffer_response.append(response_obj)
                    count += 1
                else:
                    on_tradeoffer_response.append(response_obj)
                    offer = False

            if on_tradeoffer_response[(len(on_tradeoffer_response) - 1)]['response']:
                if count % 2 == 0:
                    done = self._trade_with_player(trade_offer, giver, receiver)
                else:
                    done = self._trade_with_player(trade_offer, receiver, giver)

                if done:
                    on_tradeoffer_response[(len(on_tradeoffer_response) - 1)]['completed'] = True
                    answer_object.append(on_tradeoffer_response)

                    return answer_object

            on_tradeoffer_response[(len(on_tradeoffer_response) - 1)]['completed'] = False
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

        response = receiver['player'].on_trade_offer(trade_offer)

        if count > self.MAX_COMMERCE_DEPTH:
            json_obj['response'] = False
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
                material_quantity = getattr(trade_offer.gives, materials[i])
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

    # -- -- -- --  Board functions  -- -- -- --
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
                player_hand.remove_material([MaterialConstants.CEREAL,
                                             MaterialConstants.CLAY,
                                             MaterialConstants.WOOD,
                                             MaterialConstants.WOOL
                                             ], 1)

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
                player_hand.remove_material([MaterialConstants.CLAY,
                                             MaterialConstants.WOOD
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
            if player_hand.resources.has_this_more_materials('card'):
                player_hand.remove_material([MaterialConstants.CEREAL,
                                             MaterialConstants.MINERAL,
                                             MaterialConstants.WOOL
                                             ], 1)

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
        :param player: Número que representa al jugador a robar
        :return: int
        """
        player_obj = self.bot_manager.players[player]
        actual_player_obj = self.bot_manager.players[self.bot_manager.get_actual_player()]

        material_id = -1
        total = player_obj["resources"].get_total()
        new_total = player_obj["resources"].get_total()

        while new_total == total and total != 0:
            material_id = random.randint(0, 4)
            player_obj['resources'].remove_material(material_id, 1)
            new_total = player_obj['resources'].get_total()

        actual_player_obj['resources'].add_material(material_id, 1)

        player_obj['player'].hand = player_obj['resources']
        actual_player_obj['player'].hand = actual_player_obj['resources']
        return material_id

    def on_game_start_build_towns_and_roads(self, player):
        """
        Función que te permite poner un pueblo y una carretera. Te las pone automáticamente si no pones un nodo válido
        :param player: contador externo que indica a qué jugador le toca
        :return: node_id, road_to
        """
        # Le da a los bots 2 intentos de poner bien los pueblos y carreteras. Si no, el GameManager lo hará por ellos.
        valid_nodes = self.board.valid_starting_nodes()
        materials = []

        for count in range(3):
            node_id, road_to = self.bot_manager.players[player]['player'].on_game_start(self.board)

            if node_id in valid_nodes or count == 2:

                if count == 2:
                    node_id = valid_nodes[random.randint(0, (len(valid_nodes) - 1))]

                    possible_roads = self.board.nodes[node_id]['adjacent']
                    road_to = possible_roads[random.randint(0, len(possible_roads) - 1)]

                terrain_ids = self.board.nodes[node_id]['contacting_terrain']
                for ter_id in terrain_ids:
                    materials.append(self.board.terrain[ter_id]['terrain_type'])

                self.board.nodes[node_id]['player'] = self.turn_manager.get_whose_turn_is_it()

                # Se le dan materiales al BotManager y este a los bots para que sepan cuantos tienen en realidad
                self.bot_manager.players[player]['resources'].add_material(materials, 1)
                self.bot_manager.players[player]['player'].hand = self.bot_manager.players[player]['resources']

                self.bot_manager.players[player]['victory_points'] += 1

                # Parte carreteras
                if self.board.build_road(self.turn_manager.get_whose_turn_is_it(), node_id, road_to)['response']:
                    return node_id, road_to
                else:
                    possible_roads = self.board.nodes[node_id]['adjacent']
                    road_to = possible_roads[random.randint(0, len(possible_roads) - 1)]
                    self.board.build_road(self.turn_manager.get_whose_turn_is_it(), node_id, road_to)
                    return node_id, road_to

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
            if ((road['node_id'] not in visited_nodes) and
                    (road['player_id'] == player_id or player_id == -1) and
                    (road['player_id'] == node['player'] or node['player'] == -1)):
                visited_nodes.append(road['node_id'])

                if depth > longest_road_obj['longest_road']:
                    longest_road_obj['longest_road'] = depth
                    longest_road_obj['player'] = player_id

                longest_road_obj = self.longest_road_calculator(self.board.nodes[road['node_id']], depth + 1,
                                                                longest_road_obj, road['player_id'], visited_nodes)
        return {'longest_road': longest_road_obj['longest_road'], 'player': longest_road_obj['player']}

    def play_development_card(self, player_id, card):
        """Si la carta que llega existe en la mano del BotManager se elimina y se hace el efecto, si no, se hace
        un return nulo. Si la carta es un punto de victoria no se borra de la mano.
        Después se iguala la mano del jugador a la del BotManager para evitar trampas.
        :param player_id:
        :param card:
        :return: {}
        """

        card_obj = {}

        if card.__to_object__() in self.bot_manager.players[player_id]['development_cards'].check_hand():
            if card.type != DevelopmentCardConstants.VICTORY_POINT:
                self.bot_manager.players[player_id]['development_cards'].delete_card(card.id)  # Borramos la carta

                self.bot_manager.players[player_id]['player'].development_cards_hand.hand = \
                    self.bot_manager.players[player_id]['development_cards'].hand

        else:
            self.bot_manager.players[player_id]['player'].development_cards_hand.hand = \
                self.bot_manager.players[player_id]['development_cards'].hand  # Hacen trampas

            card_obj['played_card'] = 'none'
            card_obj['reason'] = 'Trying to use cards they don\'t have'

            return card_obj

        if card.type == DevelopmentCardConstants.KNIGHT:
            # se le suma un nuevo caballero al jugador y se le pide mover al ladrón
            self.bot_manager.players[player_id]['knights'] += 1

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

            on_moving_thief = self.bot_manager.players[player_id]['player'].on_moving_thief()
            move_thief_obj = self.move_thief(on_moving_thief['terrain'], on_moving_thief['player'])

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

            if (self.bot_manager.players[player_id]['victory_points'] +
               self.bot_manager.players[player_id]['hidden_victory_points']) >= 10:

                card_obj['played_card'] = 'victory_point'
                self.bot_manager.players[player_id]['victory_points'] = 10
            else:
                card_obj['played_card'] = 'failed_victory_point'

            return card_obj
        elif card.type == DevelopmentCardConstants.PROGRESS_CARD:

            if card.effect == DevelopmentCardConstants.MONOPOLY_EFFECT:
                # Elige material
                material_chosen = self.bot_manager.players[player_id]['player'].on_monopoly_card_use()
                material_sum = 0

                if material_chosen is None:
                    material_chosen = random.randint(0, 4)

                # Se elimina el material de la mano de todos los jugadores
                for player in self.bot_manager.players:
                    material_sum += player['resources'].get_from_id(material_chosen)
                    player['resources'].remove_material(material_chosen,
                                                        player['resources'].get_from_id(material_chosen))
                    player['player'].hand = player['resources']

                # Se le dan todos los materiales eliminados al que usó la carta
                self.bot_manager.players[player_id]['resources'].add_material(material_chosen, material_sum)
                self.bot_manager.players[player_id]['player'].hand = self.bot_manager.players[player_id]['resources']

                # Se añade al objeto el material, la suma, y las nuevas manos tras la resta de materiales
                card_obj['played_card'] = 'monopoly'
                card_obj['material_chosen'] = material_chosen
                card_obj['material_sum'] = material_sum
                for i in range(4):
                    card_obj['hand_P' + str(i)] = self.bot_manager.players[i]['resources'].resources.__to_object__()

                return card_obj

            elif card.effect == DevelopmentCardConstants.ROAD_BUILDING_EFFECT:

                # Se piden en qué puntos quieren construir carreteras
                road_nodes = self.bot_manager.players[player_id]['player'].on_road_building_card_use()
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

                    # Después del bucle ponemos donde se han construido las carreteras y devolvemos el objeto
                    card_obj['roads'] = road_nodes
                    return card_obj
                else:
                    # Si el objeto carreteras es None implica que no hay carreteras construidas
                    card_obj['roads'] = None
                    return card_obj

            elif card.effect == DevelopmentCardConstants.YEAR_OF_PLENTY_EFFECT:
                card_obj['played_card'] = 'year_of_plenty'

                # Eligen 2 materiales (puede ser el mismo 2 veces)
                materials_selected = self.bot_manager.players[player_id]['player'].on_year_of_plenty_card_use()
                card_obj['materials_selected'] = materials_selected

                if materials_selected is None:
                    material, material2 = random.randint(0, 4), random.randint(0, 4)
                    materials_selected = {'material': material, 'material_2': material2}

                # Obtienen una carta de ese material elegido
                self.bot_manager.players[player_id]['resources'].add_material(materials_selected['material'], 1)
                self.bot_manager.players[player_id]['resources'].add_material(materials_selected['material_2'], 1)

                # Se actualiza la mano
                self.bot_manager.players[player_id]['player'].hand = self.bot_manager.players[player_id]['resources']

                card_obj['hand_P' + str(player_id)] = self.bot_manager.players[player_id][
                    'resources'].resources.__to_object__()
                return card_obj
            return card_obj
        return card_obj

    def check_player_hands(self):
        for i in range(4):
            print('P' + str(i + 1))
            print(self.bot_manager.players[i]['development_cards'].check_hand())

        print('Players: ')
        for i in range(4):
            print('P' + str(i + 1))
            print(self.bot_manager.players[i]['player'].development_cards_hand.check_hand())

    def get_turn(self):
        """
        :return: int
        """
        return self.turn_manager.get_turn()

    def set_turn(self, turn=0):
        """
        :param turn: int
        :return:
        """
        self.turn_manager.set_turn(turn)
        return

    def get_whose_turn_is_it(self):
        """
        :return: int
        """
        return self.turn_manager.get_whose_turn_is_it()

    def set_whose_turn_is_it(self, turn=0):
        """
        :param turn: int
        :return:
        """
        self.turn_manager.set_whose_turn_is_it(turn)
        return

    def set_phase(self, phase=0):
        """
        :param phase: int
        :return:
        """
        self.turn_manager.set_phase(phase)
        return

    def get_round(self):
        """
        :return: int
        """
        return self.turn_manager.get_round()

    def set_round(self, round=0):
        """
        :param round: int
        :return:
        """
        self.turn_manager.set_turn(round)
        return

    def get_players(self):
        """
        :return: list
        """
        return self.bot_manager.players

    def set_actual_player(self, player_id=0):
        """
        :param player_id: int
        :return:
        """
        self.turn_manager.actual_player = player_id
        return

    def on_turn_start(self, player):
        """
        :param player: int
        :return: DevelopmentCard, None
        """
        return self.bot_manager.players[player]['player'].on_turn_start()

    def get_last_dice_roll(self):
        """
        :return: int
        """
        return self.last_dice_roll

    def player_resources_total(self, player_id):
        """
        :return: int
        """
        return self.bot_manager.players[player_id]['resources'].get_total()

    def player_resources_to_object(self, player_id):
        """
        :return: dict
        """
        return self.bot_manager.players[player_id]['resources'].resources.__to_object__()

    def call_to_bot_on_commerce_phase(self, player_id):
        """
        :param player_id: int
        :return: TradeOffer, dict{'gives': int, 'receives': int}, None
        """
        return self.bot_manager.players[player_id]['player'].on_commerce_phase()

    def call_to_bot_on_build_phase(self, player_id):
        """
        :param player_id: int
        :return: dict{'building': str, 'node_id': int, 'road_to': int/None}, None
        """
        return self.bot_manager.players[player_id]['player'].on_build_phase(self.board)

    def call_to_bot_on_turn_end(self, player_id):
        """
        :param player_id: int
        :return: DevelopmentCard, None
        """
        return self.bot_manager.players[player_id]['player'].on_turn_end()

    def get_board_nodes(self):
        """
        :return: nodes
        """
        return self.board.nodes

    def get_board_terrain(self):
        """
        :return: terrain
        """
        return self.board.terrain
