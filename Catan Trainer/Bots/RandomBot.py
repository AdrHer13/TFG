import random

from Classes.Constants import MaterialConstants, BuildConstants
from Classes.Materials import Materials
from Classes.TradeOffer import TradeOffer
from Interfaces.BotInterface import BotInterface


class RandomBot(BotInterface):
    """
    Es necesario poner super().nombre_de_funcion() para asegurarse de que coge la función del padre
    """
    def __init__(self, bot_id):
        super().__init__(bot_id)
        pass

    def on_trade_offer(self, **kwargs):
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

    def on_turn_start(self):
        # self.development_cards_hand.add_card(DevelopmentCard(99, 0, 0))
        if len(self.development_cards_hand.check_hand()) and random.randint(0, 1):
            return self.development_cards_hand.play_card_by_id(self.development_cards_hand.hand[0].id)
        return None

    def on_having_more_than_7_materials(self):
        return self.hand

    def on_moving_thief(self):
        terrain = random.randint(0, 18)
        player = -1
        for node in self.board.terrain[terrain]['contactingNodes']:
            if self.board.nodes[node]['player'] != -1:
                player = self.board.nodes[node]['player']
        return {'terrain': terrain, 'player': player}

    def on_turn_end(self):
        if len(self.development_cards_hand.check_hand()) and random.randint(0, 1):
            return self.development_cards_hand.play_card_by_id(self.development_cards_hand.hand[0].id)
        return None

    def on_commerce_phase(self):
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
        return super().on_game_start(board_instance)

    def on_monopoly_card_use(self):
        material = random.randint(0, 4)
        return material

    def on_road_building_card_use(self):
        valid_nodes = self.board.valid_road_nodes(self.id)
        if len(valid_nodes) > 1:
            while True:
                road_node = random.randint(0, len(valid_nodes) - 1)
                road_node_2 = random.randint(0, len(valid_nodes) - 1)
                if road_node != road_node_2:
                    return {'nodeID': valid_nodes[road_node]['startingNode'],
                            'roadTo': valid_nodes[road_node]['finishingNode'],
                            'nodeID_2': valid_nodes[road_node_2]['startingNode'],
                            'roadTo_2': valid_nodes[road_node_2]['finishingNode'],
                            }
        elif len(valid_nodes) == 1:
            return {'nodeID': valid_nodes[0]['startingNode'],
                    'roadTo': valid_nodes[0]['finishingNode'],
                    'nodeID_2': None,
                    'roadTo_2': None,
                    }
        return None

    def on_year_of_plenty_card_use(self):
        material, material2 = random.randint(0, 4), random.randint(0, 4)
        return {'material': material, 'material_2': material2}
