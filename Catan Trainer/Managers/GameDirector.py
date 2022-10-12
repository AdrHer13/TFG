import random

from Classes.Constants import BuildConstants, HarborConstants
from Classes.DevelopmentCards import DevelopmentCard
from Classes.Hand import Hand
from Classes.TradeOffer import TradeOffer
from Managers.GameManager import GameManager
from TraceLoader.TraceLoader import TraceLoader


class GameDirector:
    """
    Clase que se encarga de dirigir la partida, empezarla y acabarla
    """
    # turn_manager = TurnManager()
    # bot_manager = BotManager()
    game_manager = GameManager()
    trace_loader = TraceLoader()

    MAX_COMMERCE_TRADES = 2
    already_played_development_card = False

    def __init__(self):
        return

    # Turn #
    def start_turn(self, player=-1):
        """
        Esta función permite iniciar el turno
        :param player: número que representa al jugador
        :return: object
        """
        start_turn_object = {'development_card_played': []}
        print('----------')
        print('start turn: ' + str(self.game_manager.turn_manager.get_turn()))
        self.game_manager.turn_manager.set_phase(0)
        self.game_manager.bot_manager.set_actual_player(player)

        turn_start_response = self.game_manager.bot_manager.players[player]['player'].on_turn_start()

        if isinstance(turn_start_response, DevelopmentCard) and not self.already_played_development_card:
            played_card_obj = self.game_manager.play_development_card(player, turn_start_response)
            if not (played_card_obj['played_card'] == 'victory_point' or
                    played_card_obj['played_card'] == 'failed_victory_point'):
                self.already_played_development_card = True
            start_turn_object['development_card_played'].append(played_card_obj)

        self.game_manager.throw_dice()
        self.game_manager.give_resources()

        start_turn_object['dice'] = self.game_manager.last_dice_roll
        start_turn_object['actual_player'] = str(self.game_manager.turn_manager.get_whose_turn_is_it())

        print('Jugador: ' + str(self.game_manager.turn_manager.get_whose_turn_is_it()))
        # print('Resources ActualPlayer: ' + str(self.game_manager.bot_manager.players[player]['player'].hand.resources))

        for i in range(4):
            print('Resources J' + str(i) + ': ' + str(
                self.game_manager.bot_manager.players[i]['resources'].resources) + ' | Total: ' + str(
                self.game_manager.bot_manager.players[i]['resources'].get_total()))

        if self.game_manager.last_dice_roll == 7:
            for obj in self.game_manager.bot_manager.players:
                if obj['resources'].get_total():
                    total = obj['resources'].get_total()
                    if total > 7:
                        max_hand = (total / 2).__ceil__()
                        new_total = obj['player'].on_having_more_than_7_materials().get_total()

                        # print('Total: ' + str(total))
                        # print('Mano máxima: ' + str(max_hand))
                        # print('Debe descartar: ' + str(new_total - max_hand))

                        if new_total > max_hand:
                            for i in range(0, (new_total - max_hand)):
                                response = False
                                while not response:
                                    response = obj['resources'].remove_material(random.randint(0, 4), 1)
                                obj['player'].hand = obj['resources']
                        else:
                            obj['resources'] = obj['player'].hand

            print('       -     -     -     -     -     -        ')
            for i in range(4):
                print('Resources J' + str(i) + ': ' + str(
                    self.game_manager.bot_manager.players[i]['resources'].resources) + ' | Total: ' + str(
                    self.game_manager.bot_manager.players[i]['resources'].get_total()))

            on_moving_thief = self.game_manager.bot_manager.players[player]['player'].on_moving_thief()
            move_thief_obj = self.game_manager.move_thief(on_moving_thief['terrain'], on_moving_thief['player'])

            start_turn_object['past_thief_terrain'] = move_thief_obj['lastThiefTerrain']
            start_turn_object['thief_terrain'] = move_thief_obj['terrainId']
            start_turn_object['robbed_player'] = move_thief_obj['robbedPlayer']
            start_turn_object['stolen_material_id'] = move_thief_obj['stolenMaterialId']

        for i in range(4):
            start_turn_object['hand_P' + str(i)] = \
                self.game_manager.bot_manager.players[i]['resources'].resources.__to_object__()
            start_turn_object['total_P' + str(i)] = \
                str(self.game_manager.bot_manager.players[i]['resources'].get_total())

        # LLama al inicio del turno de los jugadores
        # self.game_manager.bot_manager.players[player]['player'].on_turn_start()
        return start_turn_object

    def start_commerce_phase(self, player=-1, depth=1):
        """
        Esta función permite pasar a la fase de comercio
        :param depth:
        :param player: número que representa al jugador
        :return: object
        """
        commerce_phase_object = {}

        print('Start commerce phase: ' + str(self.game_manager.turn_manager.get_turn()))

        self.game_manager.turn_manager.set_phase(1)
        commerce_response = self.game_manager.bot_manager.players[player]['player'].on_commerce_phase()

        if isinstance(commerce_response, TradeOffer) and depth <= self.MAX_COMMERCE_TRADES:
            commerce_phase_object['trade_offer'] = commerce_response.__to_object__()
            commerce_phase_object['harbor_trade'] = False

            if commerce_response:
                print('Oferta: ' + str(commerce_response))

                if self.game_manager.bot_manager.players[player]['resources'].resources.has_this_more_materials(
                        commerce_response.gives):
                    commerce_phase_object['inviable'] = False
                    print('Puede hacer la oferta')
                    answer_object = self.game_manager.send_trade_with_everyone(commerce_response)
                    commerce_phase_object['answers'] = answer_object
                else:
                    commerce_phase_object['inviable'] = True
                    # TODO: se queja de que no puede hacerla, le da una segunda oportunidad, en otro fallo
                    #       le salta la fase de comercio

            return commerce_phase_object
        elif isinstance(commerce_response, dict):
            print('%%%%%%%%%%%%%%%%%%%%%%%%%%%')
            print('Jugador comercia por puerto')
            print(self.game_manager.bot_manager.players[player]['player'].hand)

            commerce_phase_object['trade_offer'] = commerce_response
            commerce_phase_object['harbor_trade'] = True

            harbor_type = self.game_manager.board.check_for_player_harbors(player, commerce_response['gives'])
            if harbor_type == HarborConstants.NONE:
                response = self.game_manager.commerce_manager.trade_without_harbor(
                    self.game_manager.bot_manager.players[player]['resources'], commerce_response['gives'],
                    commerce_response['receives'])
            elif harbor_type == HarborConstants.ALL:
                response = self.game_manager.commerce_manager.trade_through_harbor(
                    self.game_manager.bot_manager.players[player]['resources'], commerce_response['gives'],
                    commerce_response['receives'])
            else:
                response = self.game_manager.commerce_manager.trade_through_special_harbor(
                    self.game_manager.bot_manager.players[player]['resources'], commerce_response['gives'],
                    commerce_response['receives'])

            if isinstance(response, Hand):
                commerce_phase_object['answer'] = response.resources.__to_object__()
                self.game_manager.bot_manager.players[player]['player'].hand = response
                print(self.game_manager.bot_manager.players[player]['player'].hand)
            else:
                commerce_phase_object['answer'] = response
                print('pero no tiene materiales suficientes')
            print('%%%%%%%%%%%%%%%%%%%%%%%%%%%')
            return commerce_phase_object

        elif isinstance(commerce_response, DevelopmentCard) and not self.already_played_development_card:
            played_card_obj = self.game_manager.play_development_card(player, commerce_response)
            commerce_phase_object['trade_offer'] = 'played_card'
            commerce_phase_object['harbor_trade'] = None
            commerce_phase_object['development_card_played'] = played_card_obj
            if not (played_card_obj['played_card'] == 'victory_point' or
                    played_card_obj['played_card'] == 'failed_victory_point'):
                self.already_played_development_card = True

            return commerce_phase_object
        else:
            commerce_phase_object['trade_offer'] = 'None'
            return commerce_phase_object

    def start_build_phase(self, player=-1):
        """
        Esta función permite pasar a la fase de construcción
        :param build_phase_object:
        :param player: número que representa al jugador
        :return: void
        """
        print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
        print('vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv')
        print('start build phase: ' + str(self.game_manager.turn_manager.get_turn()))
        build_phase_object = {}

        self.game_manager.turn_manager.set_phase(2)
        build_response = self.game_manager.bot_manager.players[player]['player'].on_build_phase(self.game_manager.board)
        if isinstance(build_response, dict):
            build_phase_object = build_response
            built = False
            if build_response['building'] == BuildConstants.TOWN:
                built = self.game_manager.build_town(player, build_response['nodeID'])
                if built['response']:
                    self.game_manager.bot_manager.players[player]['victoryPoints'] += 1
            elif build_response['building'] == BuildConstants.CITY:
                built = self.game_manager.build_city(player, build_response['nodeID'])
                if built['response']:
                    self.game_manager.bot_manager.players[player]['victoryPoints'] += 1
            elif build_response['building'] == BuildConstants.ROAD:
                built = self.game_manager.build_road(player, build_response['nodeID'], build_response['roadTo'])
            elif build_response['building'] == BuildConstants.CARD:
                built = self.game_manager.build_development_card(player)

            if isinstance(built, dict):
                if built['response']:
                    build_phase_object['finished'] = True

                    if build_response['building'] == BuildConstants.CARD:
                        build_phase_object['card_id'] = built['card_effect']
                        build_phase_object['card_type'] = built['card_type']
                        build_phase_object['card_effect'] = built['card_effect']

                    print('J' + str(player) + ' ha construido algo: ')
                    print(build_response)
                    # Si se ha construido permitir que vuelvan a construir
                    # print(build_phase_object)
                else:
                    build_phase_object['finished'] = False
                    print('J' + str(player) + ' ha fallado en algo: ')
                    print(build_response)
                    print(built['errorMsg'])
                    # TODO: Avisar que no se ha podido construir
            else:
                build_phase_object['finished'] = False
                build_phase_object['errorMsg'] = 'Falta de materiales'
                print('No se ha podido construir por falta de materiales')
                # TODO: Avisar que no se ha podido construir

        elif isinstance(build_response, DevelopmentCard) and not self.already_played_development_card:
            played_card_obj = self.game_manager.play_development_card(player, build_response)
            build_phase_object['building'] = 'played_card'
            build_phase_object['finished'] = 'played_card'
            build_phase_object['development_card_played'] = played_card_obj

            if not (played_card_obj['played_card'] == 'victory_point' or
                    played_card_obj['played_card'] == 'failed_victory_point'):
                self.already_played_development_card = True

            return build_phase_object
        else:
            build_phase_object['building'] = 'None'

        return build_phase_object

    def end_turn(self, player_id=-1):
        """
        Esta función permite finalizar el turno
        :param player_id: número que representa al jugador
        :return: void
        """
        print('start end turn: ' + str(self.game_manager.turn_manager.get_turn()))
        print('----- Puntos de victoria de los jugadores: ------')

        end_turn_object = {'development_card_played': []}

        self.game_manager.turn_manager.set_phase(3)
        turn_end_response = self.game_manager.bot_manager.players[player_id]['player'].on_turn_end()

        if isinstance(turn_end_response, DevelopmentCard) and not self.already_played_development_card:
            played_card_obj = self.game_manager.play_development_card(player_id, turn_end_response)
            if not (played_card_obj['played_card'] == 'victory_point' or
                    played_card_obj['played_card'] == 'failed_victory_point'):
                self.already_played_development_card = True
            end_turn_object['development_card_played'].append(played_card_obj)

        # -- -- -- -- Calcular carretera más larga -- -- -- --
        # Le quitamos el titulo al jugador que lo tiene
        for player in self.game_manager.bot_manager.players:
            if player['longest_road'] == 1:
                player['longest_road'] = 0
                player['victoryPoints'] -= 2
                break

        # Calculamos quien tiene la carretera más larga
        real_longest_road = {'longest_road': 5, 'player': -1}
        for node in self.game_manager.board.nodes:
            longest_road_obj = self.game_manager.longest_road_calculator(node, 1, {'longest_road': 0, 'player': -1}, -1,
                                                                         [node['id']])
            # print('. . . . . . . . .')
            # print('Node start: ' + str(node['id']))
            # print('Longer:')
            # print(longest_road_obj)
            if longest_road_obj['longest_road'] > real_longest_road['longest_road']:
                real_longest_road = longest_road_obj
        # Se le da el titulo a quien tenga la carretera más larga
        if real_longest_road['player'] != -1:
            self.game_manager.bot_manager.players[real_longest_road['player']]['longest_road'] = 1
            self.game_manager.bot_manager.players[real_longest_road['player']]['victoryPoints'] += 2
        # print('-- -- -- -- -- -- -- -- --')
        # print('Longest: ')
        # print(real_longest_road)
        # -- -- -- -- Fin carretera más larga -- -- -- --

        vp = {}
        for i in range(4):
            vp['J' + str(i)] = str(self.game_manager.bot_manager.players[i]['victoryPoints'])
            print('J' + str(i) + ': ' + str(self.game_manager.bot_manager.players[i]['victoryPoints']) + ' (' + str(
                self.game_manager.bot_manager.players[i]['largest_army']) + ')' + ' (' + str(
                self.game_manager.bot_manager.players[i]['longest_road']) + ')')
        print('----- FIN Puntos de victoria de los jugadores ------')

        end_turn_object['victory_points'] = vp
        return end_turn_object

    # Round #
    def round_start(self):
        """
        Esta función permite comenzar una ronda nueva
        :return:
        """
        round_object = {}
        print('---------------------')
        print('round start')
        self.already_played_development_card = False

        for i in range(4):
            obj = {}
            self.game_manager.turn_manager.set_turn(self.game_manager.turn_manager.get_turn() + 1)
            self.game_manager.turn_manager.set_whose_turn_is_it(i)

            start_turn_object = self.start_turn(self.game_manager.turn_manager.get_whose_turn_is_it())
            obj['start_turn'] = start_turn_object

            # Se permite comerciar un máximo de 2 veces con jugadores, pero cualquier cantidad con el puerto. Si se intenta
            #  comercia con un jugador una tercera vez, devuelve None y corta el bucle
            commerce_phase_array, depth = [], 1
            while True:
                commerce_phase_object = self.start_commerce_phase(self.game_manager.turn_manager.get_whose_turn_is_it(),
                                                                  depth)
                commerce_phase_array.append(commerce_phase_object)
                if commerce_phase_object['trade_offer'] == 'None':
                    break
                elif not (commerce_phase_object['harbor_trade'] or commerce_phase_object['harbor_trade'] is None):
                    depth += 1
            obj['commerce_phase'] = commerce_phase_array

            # Se puede construir cualquier cantidad de veces en un turno mientras tengan materiales. Así que para evitar un
            #  bucle infinito, se corta si se construye 'None' o si fallan al intentar construir
            build_phase_array = []
            while True:
                build_phase_object = self.start_build_phase(self.game_manager.turn_manager.get_whose_turn_is_it())
                build_phase_array.append(build_phase_object)
                if build_phase_object['building'] == 'None' or not build_phase_object['finished']:
                    break
            obj['build_phase'] = build_phase_array

            end_turn_object = self.end_turn(self.game_manager.turn_manager.get_whose_turn_is_it())
            obj['end_turn'] = end_turn_object

            round_object['turn_P' + str(i)] = obj

            print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
            print('vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv')

        return round_object

    def round_end(self):
        """
        Esta función permite acabar una ronda empezada
        :return:
        """
        print('round end')
        print('---------------------')

        winner = False
        for player in self.game_manager.bot_manager.players:
            if player['victoryPoints'] >= 10:
                # if (player['victoryPoints'] >= 10 or
                # (player['victoryPoints'] >= 8 and (player['largest_army'] == 1 or player['longest_road'] == 1)) or
                # (player['victoryPoints'] >= 6 and player['largest_army'] == 1 and player['longest_road'] == 1)):
                winner = True

        self.game_manager.turn_manager.set_round(self.game_manager.turn_manager.get_round() + 1)
        return winner

    # Game #
    def game_start(self):
        """
        Esta función permite comenzar una partida nueva
        :return:
        """
        print('game start')
        # Se cargan los bots y se inicializa el tablero
        # self.game_manager.bot_manager.load_bots()
        self.game_manager.board.__init__()

        # Se añade el tablero al setup, para que el intérprete sepa cómo es el tablero
        setup_object = {
            "board": {
                "board_nodes": self.game_manager.board.nodes,
                "board_terrain": self.game_manager.board.terrain,
            }
        }

        # Se le da paso al primer jugador para que ponga un poblado y una aldea
        for i in range(4):
            setup_object["P" + str(i)] = []
            self.game_manager.bot_manager.set_actual_player(i)
            self.game_manager.turn_manager.set_whose_turn_is_it(i)

            # función recursiva a introducir
            node_id, road_to = self.game_manager.on_game_start_built_nodes_and_roads(i)
            setup_object["P" + str(i)].append({"id": node_id, "road": road_to})

        for i in range(3, -1, -1):
            self.game_manager.bot_manager.set_actual_player(i)
            self.game_manager.turn_manager.set_whose_turn_is_it(i)

            # función recursiva a introducir
            node_id, road_to = self.game_manager.on_game_start_built_nodes_and_roads(i)
            setup_object["P" + str(i)].append({"id": node_id, "road": road_to})

        ######################################################
        ##       Por si quieres ver el tablero              ##
        ######################################################
        # print('---------------------\n')
        # print('Nodos:')
        # for node in self.game_manager.board.nodes:
        #     print('ID: ' + str(node['id']))
        #     print('Player: ' + str(node['player']))
        #     print('Roads: ')
        #     print(node['roads'])
        #     print('---------------------\n')
        # ######################################################
        # print('#######################\n')
        # print('Terreno:')
        # for terrain in self.game_manager.board.terrain:
        #     print('ID: ' + str(terrain['id']))
        #     print('Prob: ' + str(terrain['probability']))
        #     print('Type: ' + str(terrain['terrainType']))
        #     print('#######################\n')
        # ######################################################

        self.trace_loader.current_trace["setup"] = setup_object
        self.game_loop()
        return

    def game_loop(self):
        game_object = {}
        winner = False
        while not winner:
            game_object['round_' + str(self.game_manager.turn_manager.get_round())] = self.round_start()
            winner = self.round_end()

        self.trace_loader.current_trace["game"] = game_object
        self.trace_loader.export_to_file()
        return


if __name__ == '__main__':
    print('vvvvvvvvvvvvvvvvvvvvvvvvvvvvv')
    GameDirector().game_start()
    print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
