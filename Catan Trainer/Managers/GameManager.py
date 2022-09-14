#
# Clase que se encarga de dirigir una partida de Catan
#
import math
import random

from Classes.Board import Board
from Classes.Constants import MaterialConstants
from Classes.Materials import Materials
from Classes.TradeOffer import TradeOffer
from Classes.DevelopmentCards import *

from Managers.TurnManager import TurnManager
from Managers.CommerceManager import CommerceManager
from Managers.BotManager import BotManager


class GameManager:
    """
    Clase que representa el game manager, entidad que tiene todas las acciones que pueden hacer los jugadores
    """
    last_dice_roll = 0
    board = Board()
    development_cards_deck = DevelopmentDeck()
    turn_manager = TurnManager()
    commerce_manager = CommerceManager()
    bot_manager = BotManager()

    # graphics_manager = GraphicsManager()

    def __init__(self):
        self.development_cards_deck = DevelopmentDeck()
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
        print('throw dice: ' + str(self.last_dice_roll))
        return

    def give_resources(self):
        """
        Función que entrega materiales a cada uno de los jugadores en función de la tirada de dados
        :return: void
        """
        # Por cada pieza de terreno en el tablero
        for terrain in self.board.terrain:
            # Si la probabilidad coincide
            if terrain['probability'] == self.last_dice_roll:
                # Se miran los nodos adyacentes
                for node in terrain['contactingNodes']:
                    # Si tiene jugador, implica que hay pueblo
                    if self.board.nodes[node]['player'] != -1:
                        player = self.bot_manager.players[self.board.nodes[node]['player']]
                        # Si tiene ciudad se dan 2 en lugar de 1 material

                        if self.board.nodes[node]['hasCity']:
                            print('J' + str(self.board.nodes[node]['player']) + ' | material: ' + str(
                                terrain['terrainType']) + ' | amount: 2')
                            player['player'].hand.add_material(terrain['terrainType'], 2)
                            player['resources'].add_material(terrain['terrainType'], 2)
                        else:
                            print('J' + str(self.board.nodes[node]['player']) + ' | material: ' + str(
                                terrain['terrainType']) + ' | amount: 1')
                            player['player'].hand.add_material(terrain['terrainType'], 1)
                            player['resources'].add_material(terrain['terrainType'], 1)
        return None

    def send_trade_with_everyone(self, trade_offer=TradeOffer()):
        """
        Permite enviar una oferta a todos los jugadores en la mesa. Si alguno acepta se hará el intercambio
        :param trade_offer: Oferta de comercio con el jugador, debe incluir qué se entrega y qué se recibe
        :return: void
        """
        # receivers = self.bot_manager.get_other_players_except_int(self.turn_manager.whoseTurnIsIt)
        answer_object = []

        receivers = []
        for index in range(4):
            if index != self.turn_manager.whoseTurnIsIt:
                receivers.append(self.bot_manager.players[index])

        # Se aleatorizan el orden en el que se va a recibir la oferta para evitar que J1 tenga ventaja
        current_index, random_index = len(receivers), 0
        while current_index != 0:
            random_index = math.floor(random.random() * current_index)
            current_index -= 1
            (receivers[current_index], receivers[random_index]) = (receivers[random_index], receivers[current_index])

        giver = self.bot_manager.players[self.turn_manager.whoseTurnIsIt]
        for receiver in receivers:
            on_tradeoffer_response = []

            repeat, count = True, 1
            while repeat:
                # Se hace un bucle de contraofertas hasta que se llegue a una decisión de True o False
                if count % 2 == 0:
                    # Giver toma el papel de receiver porque es una contraoferta
                    response_obj = self.on_tradeoffer_response(giver, receiver, count, trade_offer)
                else:
                    response_obj = self.on_tradeoffer_response(receiver, giver, count, trade_offer)

                on_tradeoffer_response.append(response_obj)
                if isinstance(response_obj['response'], dict):
                    repeat = True
                    count += 1
                else:
                    repeat = False

            if on_tradeoffer_response[(len(on_tradeoffer_response) - 1)]['response']:
                if count % 2 == 0:
                    print('J' + str(self.turn_manager.whoseTurnIsIt) + ' ha aceptado')
                    done = self.trade_with_player(trade_offer, giver, receiver)
                else:
                    print('J' + str(receiver['id']) + ' ha aceptado')
                    done = self.trade_with_player(trade_offer, receiver, giver)

                if done:
                    on_tradeoffer_response[(len(on_tradeoffer_response) - 1)]['completed'] = True
                    answer_object.append(on_tradeoffer_response)
                    return answer_object
                else:
                    on_tradeoffer_response[(len(on_tradeoffer_response) - 1)]['completed'] = False
            else:
                print('J' + str(receiver['id']) + ' ha negado')
            answer_object.append(on_tradeoffer_response)
        return answer_object

    def on_tradeoffer_response(self, receiver, giver, count, trade_offer):
        """
        Función llamada cuando llega una oferta de comercio como respuesta a una oferta de comercio
        :param giver: Player()
        :param receiver: Player()
        :param count: Int
        :param json_obj: Objeto json al que se le añaden datos para poder exportarlo correctamente
        :param trade_offer: TradeOffer()
        :return: dictionary {'count': int, 'giver': Player(), 'receiver': Player(), 'trade_offer': TradeOffer(), 'response': True/False}
        """
        json_obj = {
            'count': count,
            'trade_offer': trade_offer.__to_object__(),
            'giver': giver['id'],
            'receiver': receiver['id'],
        }

        response = receiver['player'].on_trade_offer(trade_offer)
        if isinstance(response, TradeOffer):
            if count > 2:
                json_obj['response'] = False
                return json_obj

            else:
                # Se pasa de vuelta al bucle para que rote giver y receiver y se vuelva a preguntar por respuesta
                json_obj['response'] = response.__to_object__()
                return json_obj
        else:
            json_obj['response'] = response
            return json_obj

    def trade_with_player(self, trade_offer=None, giver=None, receiver=None):
        """
        Función que hace el intercambio entre dos jugadores
        :param trade_offer: TradeOffer()
        :param giver: {BotInterface(), Hand(), int, DevelopmentCardHand()}
        :param receiver: {BotInterface(), Hand(), int, DevelopmentCardHand()}
        :return: bool
        """
        if trade_offer is None or giver is None or receiver is None:
            return False

        # Si receiver o giver no tiene materiales se le ignora
        if (receiver['resources'].resources.has_this_more_materials(trade_offer.receives) and
                giver['resources'].resources.has_this_more_materials(trade_offer.gives)):
            print('Puede hacerse el intercambio: ')
            # Se hace el intercambio

            print('Giver: ' + str(giver['resources']))
            print('Receiver: ' + str(receiver['resources']))
            # Se resta lo que da del giver
            giver['resources'].remove_material(MaterialConstants.WOOL, trade_offer.gives.wool)
            giver['resources'].remove_material(MaterialConstants.WOOD, trade_offer.gives.wood)
            giver['resources'].remove_material(MaterialConstants.CLAY, trade_offer.gives.clay)
            giver['resources'].remove_material(MaterialConstants.CEREAL, trade_offer.gives.cereal)
            giver['resources'].remove_material(MaterialConstants.MINERAL, trade_offer.gives.mineral)

            # Se añade lo que recibe
            giver['resources'].add_material(MaterialConstants.WOOL, trade_offer.receives.wool)
            giver['resources'].add_material(MaterialConstants.WOOD, trade_offer.receives.wood)
            giver['resources'].add_material(MaterialConstants.CLAY, trade_offer.receives.clay)
            giver['resources'].add_material(MaterialConstants.CEREAL, trade_offer.receives.cereal)
            giver['resources'].add_material(MaterialConstants.MINERAL, trade_offer.receives.mineral)

            # Se resta lo que receiver entrega
            receiver['resources'].remove_material(MaterialConstants.WOOL, trade_offer.receives.wool)
            receiver['resources'].remove_material(MaterialConstants.WOOD, trade_offer.receives.wood)
            receiver['resources'].remove_material(MaterialConstants.CLAY, trade_offer.receives.clay)
            receiver['resources'].remove_material(MaterialConstants.CEREAL, trade_offer.receives.cereal)
            receiver['resources'].remove_material(MaterialConstants.MINERAL, trade_offer.receives.mineral)

            # Se añade lo que receiver recibe
            receiver['resources'].add_material(MaterialConstants.WOOL, trade_offer.gives.wool)
            receiver['resources'].add_material(MaterialConstants.WOOD, trade_offer.gives.wood)
            receiver['resources'].add_material(MaterialConstants.CLAY, trade_offer.gives.clay)
            receiver['resources'].add_material(MaterialConstants.CEREAL, trade_offer.gives.cereal)
            receiver['resources'].add_material(MaterialConstants.MINERAL, trade_offer.gives.mineral)

            giver['player'].hand = giver['resources']
            receiver['player'].hand = receiver['resources']
            print('-------------------------')
            print('Giver: ' + str(giver['resources']))
            print('Receiver: ' + str(receiver['resources']))
            return True
        else:
            print('No tienen materiales suficientes para completar la oferta')
            return False

    ########### Board functions ###################
    def build_town(self, player_id, node):
        """
        Permite construir un pueblo en el nodo seleccionado
        :param player_id: Número que representa al jugador
        :param node: Número que representa un nodo en el tablero
        :return: void
        """
        player_hand = self.bot_manager.players[player_id]['resources']
        if player_hand.resources.has_this_more_materials(Materials(1, 0, 1, 1, 1)):
            build_town_obj = self.board.build_town(self.turn_manager.get_whose_turn_is_it(), node)

            if build_town_obj['response']:
                player_hand.remove_material(MaterialConstants.CEREAL, 1)
                player_hand.remove_material(MaterialConstants.CLAY, 1)
                player_hand.remove_material(MaterialConstants.WOOD, 1)
                player_hand.remove_material(MaterialConstants.WOOL, 1)
                self.bot_manager.players[player_id]['player'].hand = player_hand

            return build_town_obj
        else:
            return False

    def build_city(self, player_id, node):
        """
        Permite construir una ciudad en el nodo seleccionado
        :param player_id: Número que representa al jugador
        :param node: Número que representa un nodo en el tablero
        :return: void
        """
        player_hand = self.bot_manager.players[player_id]['resources']
        if player_hand.resources.has_this_more_materials(Materials(2, 3, 0, 0, 0)):
            build_city_obj = self.board.build_city(self.turn_manager.get_whose_turn_is_it(), node)

            if build_city_obj['response']:
                player_hand.remove_material(MaterialConstants.CEREAL, 2)
                player_hand.remove_material(MaterialConstants.MINERAL, 3)
                self.bot_manager.players[player_id]['player'].hand = player_hand

            return build_city_obj
        else:
            return False

    def build_road(self, player_id, node, road):
        """
        Permite construir una carretera en el camino seleccionado
        :param player_id: Número que representa al jugador
        :param node: Número que representa
        :param road: Número que representa una carretera en el tablero
        :return: void
        """
        player_hand = self.bot_manager.players[player_id]['resources']
        if player_hand.resources.has_this_more_materials(Materials(0, 0, 1, 1, 0)):
            build_road_obj = self.board.build_road(self.turn_manager.get_whose_turn_is_it(), node, road)

            if build_road_obj['response']:
                player_hand.remove_material(MaterialConstants.CLAY, 1)
                player_hand.remove_material(MaterialConstants.WOOD, 1)

            return build_road_obj
        else:
            return False

    def build_development_card(self, player_id):
        """
        Permite construir una carta de desarrollo
        :param player_id:
        :return:
        """
        player_hand = self.bot_manager.players[player_id]['resources']
        if player_hand.resources.has_this_more_materials(Materials(1, 1, 0, 0, 1)):
            player_hand.remove_material(MaterialConstants.CEREAL, 1)
            player_hand.remove_material(MaterialConstants.MINERAL, 1)
            player_hand.remove_material(MaterialConstants.WOOL, 1)

            self.bot_manager.players[player_id]['development_cards'].add_card(self.development_cards_deck.draw_card())
            self.bot_manager.players[player_id]['player'].development_cards_hand = self.bot_manager.players[player_id]['development_cards']
            return {'response': True}
        else:
            return False

    def move_thief(self, terrain, adjacent_player):
        """
        Permite mover al ladrón a la casilla de terreno seleccionada y en caso de que haya un poblado o ciudad de otro
        jugador adyacente a dicha casilla permite robarle un material aleatorio de la mano.
        :param terrain: Número que representa un hexágono en el tablero
        :param adjacent_player: Número de un jugador que esté adyacente al hexágono seleccionado
        :return: void
        """
        move_thief_obj = self.board.move_thief(terrain)
        move_thief_obj['robbedPlayer'] = -1
        move_thief_obj['stolenMaterialId'] = -1
        if move_thief_obj['response']:
            if adjacent_player != -1:
                for node in self.board.terrain[move_thief_obj['terrainId']]['contactingNodes']:
                    if self.board.nodes[node]['player'] == adjacent_player:
                        move_thief_obj['stolenMaterialId'] = self.__steal_from_player__(adjacent_player)
                        move_thief_obj['robbedPlayer'] = adjacent_player
                        break
                    else:
                        move_thief_obj['errorMsg'] =\
                            'No se ha podido robar al jugador debido a que no está en un nodo adyacente'
        return move_thief_obj

    def __steal_from_player__(self, player):
        """
        Función que permite robar de manera aleatoria un material de la mano de un jugador.
        :param player: Número que representa a un jugador
        :return: void
        """
        player_obj = self.bot_manager.players[player]
        actual_player_obj = self.bot_manager.players[self.bot_manager.get_actual_player()]
        material_array = []

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

    def on_game_start_built_nodes_and_roads(self, player):
        """
        Función que te permite poner un pueblo y una carretera. Te las pone automáticamente si no pones un nodo válido
        :param player: contador externo que indica a qué jugador le toca
        :param count: contador interno que lleva la cuenta de cuantas veces han intentado poner un nodo
        :return: node_id, road_to
        """

        for count in range(3):
            if count < 2:
                node_id, road_to = self.bot_manager.players[player]['player'].on_game_start(self.board)

                if (self.board.nodes[node_id]['player'] == -1
                        and self.board.adyacent_nodes_dont_have_towns(node_id)
                        and not self.board.is_it_a_coastal_node(node_id)):

                    # print('______________________')
                    # print('NODO: ' + str(node_id))

                    terrain_ids = self.board.nodes[node_id]['contactingTerrain']
                    materials = []
                    for ter_id in terrain_ids:
                        materials.append(self.board.terrain[ter_id]['terrainType'])
                    self.board.nodes[node_id]['player'] = self.turn_manager.get_whose_turn_is_it()
                    # print('Materiales del nodo de J' + str(self.board.nodes[node_id]['player']))
                    # print(materials)

                    # Se le dan materiales a la mano del botManager a la de los bots para que sepan cuantos tienen en realidad
                    self.bot_manager.players[player]['resources'].add_material(materials, 1)
                    self.bot_manager.players[player]['player'].hand.add_material(materials, 1)

                    self.bot_manager.players[player]['victoryPoints'] += 1

                    # Parte carreteras
                    if self.board.nodes[node_id]['player'] == self.turn_manager.get_whose_turn_is_it():
                        response = self.board.build_road(self.turn_manager.get_whose_turn_is_it(), node_id, road_to)
                        if not response['response']:
                            print(response['errorMsg'])
                        else:
                            print('J' + str(self.turn_manager.get_whose_turn_is_it()))
                            print('actual_node_id: ' + str(node_id) + ' | actual_road_to: ' + str(road_to))
                            return node_id, road_to
                    else:
                        print("el jugador " + str(self.turn_manager.get_whose_turn_is_it()) +
                              " ha intentado poner una carretera en un nodo que no le pertenece: " + str(road_to))

            else:
                illegal = True
                random_node_id = 0
                while illegal:
                    # random_node_id = random.randint(0, 53)
                    valid_nodes = self.board.valid_starting_nodes()
                    i = random.randint(0, (valid_nodes.__len__() - 1))
                    random_node_id = valid_nodes[i]
                    if (self.board.nodes[random_node_id]['player'] == -1 and
                            self.board.adyacent_nodes_dont_have_towns(random_node_id) and
                            not self.board.is_it_a_coastal_node(random_node_id)):
                        illegal = False
                    else:
                        illegal = True

                terrain_ids = self.board.nodes[random_node_id]['contactingTerrain']
                materials = []
                for ter_id in terrain_ids:
                    materials.append(self.board.terrain[ter_id]['terrainType'])

                self.board.nodes[random_node_id]['player'] = self.turn_manager.get_whose_turn_is_it()

                # Se le dan materiales a la mano del botManager a la de los bots para que sepan cuantos tienen en realidad
                self.bot_manager.players[player]['resources'].add_material(materials, 1)
                self.bot_manager.players[player]['player'].hand.add_material(materials, 1)

                self.bot_manager.players[player]['victoryPoints'] += 1

                illegal = True
                while illegal:
                    possible_roads = self.board.nodes[random_node_id]['adjacent']
                    random_road_to = possible_roads[random.randint(0, len(possible_roads) - 1)]

                    response = self.board.build_road(self.turn_manager.get_whose_turn_is_it(), random_node_id,
                                                     random_road_to)
                    if response['response']:
                        print('J' + str(self.turn_manager.get_whose_turn_is_it()))
                        print('random_node_id: ' + str(random_node_id) + ' | random_road_to: ' + str(random_road_to))
                        return random_node_id, random_road_to
                    else:
                        illegal = True
                        print(response['errorMsg'])

    def play_development_card(self, card):
        print('se juega una carta de desarrollo')
        print(card)
        pass
