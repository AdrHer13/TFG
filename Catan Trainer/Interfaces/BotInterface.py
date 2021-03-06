import random

from Classes.Board import Board
from Classes.Hand import Hand
from Classes.Materials import Materials
from Classes.TradeOffer import TradeOffer
from Classes.Constants import MaterialConstants, BuildConstants


class BotInterface:
    """
    Interfaz que implementa a un bot
    """
    hand = Hand()
    board = Board()
    materialConstants = MaterialConstants()
    # TODO: no debe de tener una ID de esta manera. Porque como mínimo rompen el GameDirector
    id = 0

    def __init__(self, bot_id=0):
        self.hand = Hand()
        self.board = Board()
        self.materialConstants = MaterialConstants()
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
        answer = random.randint(0, 2)
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

    # def on_turn_start(self):
    #     """
    #     Trigger para cuando empieza el turno (muy probablemente innecesarios). Termina cuando hace un return
    #     :return: void, None
    #     """
    #     print('Player on turn start')
    #     return None

    def on_having_more_than_7_materials(self):
        """
        Trigger que se llama cuando se debe descartar materiales. Si no los descarta el bot, los descartará
        el GameDirector aleatoriamente.
        :return: Hand()
        """
        return self.hand

    def on_moving_thief(self):
        """
        Trigger para cuando sale un 7 en el dado. Esto obliga a mover al ladrón. Si no se hace el GameDirector
        lo hará de manera aleatoria. Incluyendo robar 1 recurso de cualquier jugador adyacente a la ficha de terreno
        seleccionada
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
        Trigger para cuando acaba el turno (muy probablemente innecesarios). Termina cuando hace un return
        :return: void, None
        """
        print('Player on turn end')
        return None

    def on_commerce_phase(self):
        """
        Trigger para cuando empieza la fase de comercio. Devuelve una oferta
        :return: TradeOffer, Dictionary, None
        """
        print('Player on commerce phase')
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
        answer = random.randint(0, 1)
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
        elif self.hand.resources.has_this_more_materials(BuildConstants.CARD):
            return None

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
