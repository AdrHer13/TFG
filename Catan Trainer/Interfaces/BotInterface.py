import random

from Classes.Board import Board
from Classes.Hand import Hand
from Classes.Materials import Materials
from Classes.TradeOffer import TradeOffer
from Classes.Constants import MaterialConstants, BuildConstants
from Classes.DevelopmentCards import *


class BotInterface:
    """
    Interfaz que implementa a un bot
    """
    materialConstants = MaterialConstants()
    board = Board()
    hand = Hand()
    development_cards_hand = DevelopmentCardsHand()
    id = 0

    def __init__(self, bot_id):
        self.hand = Hand()
        self.board = Board()
        self.materialConstants = MaterialConstants()
        self.development_cards_hand = DevelopmentCardsHand()
        self.id = bot_id
        pass

    # Los triggers son llamados por el GameDirector las veces que sean necesarias hasta que devuelvan null
    #  o el GameDirector le niegue continuar el trigger
    def on_trade_offer(self, incoming_trade_offer=TradeOffer()):
        """
        Trigger para cuando llega una oferta. Devuelve si la acepta, la niega o envía una contraoferta
        :param incoming_trade_offer: Oferta de comercio que le llega al bot
        :return: true, TradeOffer, false, None
        """
        answer = random.randint(0, 1)
        if answer:
            if answer == 2:
                gives = Materials(random.randint(0, self.hand.get_cereal()), random.randint(0, self.hand.get_mineral()),
                                  random.randint(0, self.hand.get_clay()), random.randint(0, self.hand.get_wood()),
                                  random.randint(0, self.hand.get_wool()))
                receives = Materials(random.randint(0, self.hand.get_cereal()),
                                     random.randint(0, self.hand.get_mineral()),
                                     random.randint(0, self.hand.get_clay()), random.randint(0, self.hand.get_wood()),
                                     random.randint(0, self.hand.get_wool()))
                return TradeOffer(gives, receives)
            else:
                return True
        else:
            return False

    def on_turn_start(self):
        """
        Trigger para cuando empieza el turno. Termina cuando hace un return. Se hace antes que tirar dados. Sirve para jugar cartas de desarrollo
        :return: void, None
        """
        print('Player on turn start')
        if len(self.development_cards_hand.check_hand()) and random.randint(0, 1):
            return self.development_cards_hand.play_card_by_id(self.development_cards_hand.hand[0].id)
        return None

    def on_having_more_than_7_materials(self):
        """
        Trigger que se llama cuando se debe descartar materiales. Si no los descarta el bot, los descartará
        el GameDirector aleatoriamente.
        :return: Hand()
        """
        return self.hand

    def on_moving_thief(self):
        """
        Trigger para cuando sale un 7 en el dado o se usa una carta de soldado. Esto obliga a mover al ladrón.
        Si no se hace el GameDirector lo hará de manera aleatoria. Incluyendo robar 1 recurso de cualquier
        jugador adyacente a la ficha de terreno seleccionada
        :return: {terrain, player}
        """
        terrain = random.randint(0, 18)
        player = -1
        for node in self.board.terrain[terrain]['contactingNodes']:
            if self.board.nodes[node]['player'] != -1:
                player = self.board.nodes[node]['player']
        return {'terrain': terrain, 'player': player}

    def on_turn_end(self):
        """
        Trigger para cuando acaba el turno. Termina cuando hace un return. Sirve para jugar cartas de desarrollo
        :return: void, None
        """
        print('Player on turn end')
        if len(self.development_cards_hand.check_hand()) and random.randint(0, 1):
            return self.development_cards_hand.play_card_by_id(self.development_cards_hand.hand[0].id)
        return None

    def on_commerce_phase(self):
        """
        Trigger para cuando empieza la fase de comercio. Devuelve una oferta
        :return: TradeOffer, Dictionary, None
        """
        print('Player on commerce phase')

        if len(self.development_cards_hand.check_hand()) and random.randint(0, 1):
            return self.development_cards_hand.play_card_by_id(self.development_cards_hand.hand[0].id)

        answer = random.randint(0, 1)
        if answer:
            print(' - Jugador intenta comerciar por puerto - ')
            if self.hand.get_cereal() >= 4:
                return {'gives': MaterialConstants.CEREAL, 'receives': MaterialConstants.MINERAL}
            if self.hand.get_mineral() >= 4:
                return {'gives': MaterialConstants.MINERAL, 'receives': MaterialConstants.CEREAL}
            if self.hand.get_clay() >= 4:
                return {'gives': MaterialConstants.CLAY, 'receives': MaterialConstants.CEREAL}
            if self.hand.get_wood() >= 4:
                return {'gives': MaterialConstants.WOOD, 'receives': MaterialConstants.CEREAL}
            if self.hand.get_wool() >= 4:
                return {'gives': MaterialConstants.WOOL, 'receives': MaterialConstants.CEREAL}
            print('Jugador no quiere comerciar')
            return None
        else:
            gives = Materials(random.randint(0, self.hand.get_cereal()), random.randint(0, self.hand.get_mineral()),
                              random.randint(0, self.hand.get_clay()), random.randint(0, self.hand.get_wood()),
                              random.randint(0, self.hand.get_wool()))
            receives = Materials(random.randint(0, self.hand.get_cereal()), random.randint(0, self.hand.get_mineral()),
                                 random.randint(0, self.hand.get_clay()), random.randint(0, self.hand.get_wood()),
                                 random.randint(0, self.hand.get_wool()))
            trade_offer = TradeOffer(gives, receives)
            return trade_offer

    def on_build_phase(self, board_instance):
        """
        Trigger para cuando empieza la fase de construcción. Devuelve un string indicando qué quiere construir
        :return: dict{'building': str, 'nodeID': int, 'roadTo': int/None}, None
        """
        print('Player on build phase')
        self.board = board_instance

        if len(self.development_cards_hand.check_hand()) and random.randint(0, 1):
            return self.development_cards_hand.play_card_by_id(self.development_cards_hand.hand[0].id)

        answer = random.randint(0, 2)
        # Pueblo / carretera
        if self.hand.resources.has_this_more_materials(BuildConstants.TOWN) and answer == 0:
            answer = random.randint(0, 1)
            # Elegimos aleatoriamente si hacer un pueblo o una carretera
            if answer:
                valid_nodes = self.board.valid_town_nodes(self.id)
                if len(valid_nodes):
                    town_node = random.randint(0, len(valid_nodes) - 1)
                    return {'building': BuildConstants.TOWN, 'nodeID': valid_nodes[town_node]}
            else:
                valid_nodes = self.board.valid_road_nodes(self.id)
                if len(valid_nodes):
                    road_node = random.randint(0, len(valid_nodes) - 1)
                    return {'building': BuildConstants.ROAD,
                            'nodeID': valid_nodes[road_node]['startingNode'],
                            'roadTo': valid_nodes[road_node]['finishingNode']}

        # Ciudad
        elif self.hand.resources.has_this_more_materials(BuildConstants.CITY) and answer == 1:
            valid_nodes = self.board.valid_city_nodes(self.id)
            if len(valid_nodes):
                city_node = random.randint(0, len(valid_nodes) - 1)
                return {'building': BuildConstants.CITY, 'nodeID': valid_nodes[city_node]}

        # Carta de desarrollo
        elif self.hand.resources.has_this_more_materials(BuildConstants.CARD) and answer == 2:
            return {'building': BuildConstants.CARD}

        return None

    def on_game_start(self, board_instance):
        """
        Se llama únicamente al inicio de la partida y sirve para colocar 1 pueblo y una carretera adyacente en el mapa
        :return:
        """
        self.board = board_instance

        node_id = random.randint(0, 53)
        possible_roads = self.board.nodes[node_id]['adjacent']

        return node_id, possible_roads[random.randint(0, len(possible_roads) - 1)]

    def on_monopoly_card_use(self):
        """
        Se elige un material. El resto de jugadores te entregan dicho material
        0: Cereal
        1: Mineral
        2: Clay
        3: Wood
        4: Wool
        :return: int, representa el material elegido
        """
        material = random.randint(0, 4)
        return material

    def on_road_building_card_use(self):
        """
        Se eligen 2 lugares válidos donde construir carreteras. Si no son válidos, el programa pondrá aleatorios
        :return:
        """
        valid_nodes = self.board.valid_road_nodes(self.id)
        if len(valid_nodes) > 1:
            while True:
                road_node = random.randint(0, len(valid_nodes) - 1)
                road_node_2 = random.randint(0, len(valid_nodes) - 1)
                if road_node != road_node_2:
                    return {'nodeID': valid_nodes[road_node]['startingNode'],
                            'roadTo': valid_nodes[road_node]['finishingNode'],
                            'nodeID_2': valid_nodes[road_node]['startingNode'],
                            'roadTo_2': valid_nodes[road_node]['finishingNode'],
                            }
        elif len(valid_nodes) == 1:
            return {'nodeID': valid_nodes[0]['startingNode'],
                    'roadTo': valid_nodes[0]['finishingNode'],
                    'nodeID_2': None,
                    'roadTo_2': None,
                    }
        return None

    def on_year_of_plenty_card_use(self):
        """
        Se eligen dos materiales (puede elegirse el mismo 2 veces). Te llevas una carta de ese material
        :return:
        """
        material, material2 = random.randint(0, 4), random.randint(0, 4)
        return {'material': material, 'material_2': material2}
