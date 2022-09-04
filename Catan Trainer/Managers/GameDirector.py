import random

from Classes.Constants import BuildConstants
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

    def __init__(self):
        return

    # Turn #
    def start_turn(self, player=-1):
        """
        Esta función permite iniciar el turno
        :param player: número que representa al jugador
        :return: object
        """
        start_turn_object = {}
        print('----------')
        print('start turn: ' + str(self.game_manager.turn_manager.get_turn()))
        self.game_manager.turn_manager.set_phase(0)
        self.game_manager.bot_manager.set_actual_player(player)

        self.game_manager.throw_dice()
        self.game_manager.give_resources()
        # self.game_manager.give_all_resources()

        start_turn_object['dice'] = self.game_manager.last_dice_roll
        start_turn_object['actual_player'] = str(self.game_manager.turn_manager.get_whose_turn_is_it())

        print('Jugador: ' + str(self.game_manager.turn_manager.get_whose_turn_is_it()))
        # print('Resources ActualPlayer: ' + str(self.game_manager.bot_manager.players[player]['player'].hand.resources))

        for i in range(4):
            print('Resources J' + str(i) + ': ' + str(
                self.game_manager.bot_manager.players[i]['player'].hand.resources) + ' | Total: ' + str(
                self.game_manager.bot_manager.players[i]['player'].hand.get_total()))

        if self.game_manager.last_dice_roll == 7:
            for obj in self.game_manager.bot_manager.players:
                if obj['player'].hand.get_total():
                    total = obj['player'].hand.get_total()
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
                                    response = obj['player'].hand.remove_material(random.randint(0, 4), 1)

            for i in range(4):
                print('Resources J' + str(i) + ': ' + str(
                    self.game_manager.bot_manager.players[i]['player'].hand.resources) + ' | Total: ' + str(
                    self.game_manager.bot_manager.players[i]['player'].hand.get_total()))

            on_moving_thief = self.game_manager.bot_manager.players[player]['player'].on_moving_thief()
            # TODO: pasar terrain_id al objeto para saber donde se ha puesto el ladrón
            move_thief_obj = self.game_manager.move_thief(on_moving_thief['terrain'], on_moving_thief['player'])

            start_turn_object['past_thief_terrain'] = move_thief_obj['lastThiefTerrain']
            start_turn_object['thief_terrain'] = move_thief_obj['terrainId']
            start_turn_object['robbed_player'] = move_thief_obj['robbedPlayer']
            start_turn_object['stolen_material_id'] = move_thief_obj['stolenMaterialId']

        for i in range(4):
            start_turn_object['hand_P' + str(i)] = \
                self.game_manager.bot_manager.players[i]['player'].hand.resources.__to_object__()
            start_turn_object['total_P' + str(i)] = \
                str(self.game_manager.bot_manager.players[i]['player'].hand.get_total())

        # LLama al inicio del turno de los jugadores
        # self.game_manager.bot_manager.players[player]['player'].on_turn_start()
        return start_turn_object

    def start_commerce_phase(self, player=-1, commerce_phase_array=None):
        """
        Esta función permite pasar a la fase de comercio
        :param commerce_phase_array:
        :param player: número que representa al jugador
        :return: object
        TODO: He creado el array únicamente para poder hacerlo recursivo, dado que técnicamente un jugador debe de
                poder hacer X cantidad de comercios
        """
        if commerce_phase_array is None:
            commerce_phase_array = []
        commerce_phase_object = {}

        # TODO: Comprobar que el trade offer es valido. Es decir, no da más materiales de los que tiene
        print('Start commerce phase: ' + str(self.game_manager.turn_manager.get_turn()))
        self.game_manager.turn_manager.set_phase(1)
        trade_offer = self.game_manager.bot_manager.players[player]['player'].on_commerce_phase()
        if isinstance(trade_offer, TradeOffer):
            commerce_phase_object['trade_offer'] = trade_offer.__to_object__()
            commerce_phase_object['harbor_trade'] = False
            if trade_offer:
                print('Oferta: ' + str(trade_offer))
                # TODO: comprobar que los materiales de gives sean menores que los materiales del jugador
                if self.game_manager.bot_manager.players[player]['player'].hand.resources.has_this_more_materials(
                        trade_offer.gives):
                    commerce_phase_object['inviable'] = False
                    print('Puede hacer la oferta')
                    answer_object = self.game_manager.trade_with_everyone(trade_offer)
                    commerce_phase_object['answers'] = answer_object
                else:
                    commerce_phase_object['inviable'] = True
                    # TODO: se queja de que no puede hacerla, le da una segunda oportunidad, en otro fallo
                    #       le salta la fase de comercio

            commerce_phase_array.append(commerce_phase_object)
            return commerce_phase_array

        elif isinstance(trade_offer, dict):
            print('%%%%%%%%%%%%%%%%%%%%%%%%%%%')
            print('Jugador comercia por puerto')
            print(self.game_manager.bot_manager.players[player]['player'].hand)

            commerce_phase_object['trade_offer'] = trade_offer
            commerce_phase_object['harbor_trade'] = True

            # TODO: Hacer que tener puerto sea funcional
            response = self.game_manager.commerce_manager.trade_without_harbor(
                self.game_manager.bot_manager.players[player]['player'], trade_offer['gives'], trade_offer['receives'])
            # self.game_manager.commerce_manager.trade_through_harbor(self.game_manager.bot_manager.actualPlayer,
            #                                                         trade_offer['gives'], trade_offer['receives'])
            # self.game_manager.commerce_manager.trade_through_special_harbor(self.game_manager.bot_manager.actualPlayer,
            #                                                                 trade_offer['gives'],
            #                                                                 trade_offer['receives'])
            if isinstance(response, Hand):
                # TODO: solo devolver los materiales y cambiar la mano en el visualizador
                commerce_phase_object['answer'] = response.resources.__to_object__()
                self.game_manager.bot_manager.players[player]['player'].hand = response
                print(self.game_manager.bot_manager.players[player]['player'].hand)
            else:
                commerce_phase_object['answer'] = response
                print('pero no tiene materiales suficientes')
            print('%%%%%%%%%%%%%%%%%%%%%%%%%%%')
            commerce_phase_array.append(commerce_phase_object)
            return commerce_phase_array
        else:
            commerce_phase_object['trade_offer'] = 'None'
            commerce_phase_array.append(commerce_phase_object)
            return commerce_phase_array

    def start_build_phase(self, player=-1, build_phase_object=None):
        """
        Esta función permite pasar a la fase de construcción
        :param build_phase_object:
        :param player: número que representa al jugador
        :return: void
        """
        if build_phase_object is None:
            build_phase_object = []
        print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
        print('vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv')
        print('start build phase: ' + str(self.game_manager.turn_manager.get_turn()))
        building_obj = {}

        self.game_manager.turn_manager.set_phase(2)
        to_build = self.game_manager.bot_manager.players[player]['player'].on_build_phase(self.game_manager.board)
        if isinstance(to_build, dict):
            building_obj = to_build
            built = False
            if to_build['building'] == BuildConstants.TOWN:
                built = self.game_manager.build_town(player, to_build['nodeID'])
                if built['response']:
                    self.game_manager.bot_manager.players[player]['victoryPoints'] += 1
            elif to_build['building'] == BuildConstants.CITY:
                built = self.game_manager.build_city(player, to_build['nodeID'])
                if built['response']:
                    self.game_manager.bot_manager.players[player]['victoryPoints'] += 1
            elif to_build['building'] == BuildConstants.ROAD:
                built = self.game_manager.build_road(player, to_build['nodeID'], to_build['roadTo'])
            elif to_build['building'] == BuildConstants.CARD:
                built = self.game_manager.build_development_card(player)
                # TODO
                return build_phase_object

            if isinstance(built, dict):
                if built['response']:
                    building_obj['finished'] = True
                    print('J' + str(player) + ' ha construido algo: ')
                    print(to_build)
                    # Si se ha construido permitir que vuelvan a construir
                    build_phase_object.append(building_obj)
                    print(build_phase_object)
                    return self.start_build_phase(player, build_phase_object)
                else:
                    building_obj['finished'] = False
                    print('J' + str(player) + ' ha fallado en algo: ')
                    print(to_build)
                    print(built['errorMsg'])
                    # TODO: Avisar que no se ha podido construir
            else:
                building_obj['finished'] = False
                building_obj['errorMsg'] = 'Falta de materiales'
                print('No se ha podido construir por falta de materiales')
                # TODO: Avisar que no se ha podido construir
        else:
            building_obj['building'] = None

        build_phase_object.append(building_obj)
        return build_phase_object

    def end_turn(self, player=-1):
        """
        Esta función permite finalizar el turno
        :param player: número que representa al jugador
        :return: void
        """
        print('start end turn: ' + str(self.game_manager.turn_manager.get_turn()))
        print('----- Puntos de victoria de los jugadores: ------')

        end_turn_object = {}

        vp = {}
        for i in range(4):
            vp['J' + str(i)] = str(self.game_manager.bot_manager.players[i]['victoryPoints'])
            print('J' + str(i) + ': ' + str(self.game_manager.bot_manager.players[i]['victoryPoints']))
        print('----- FIN Puntos de victoria de los jugadores ------')
        self.game_manager.turn_manager.set_phase(3)
        self.game_manager.bot_manager.players[player]['player'].on_turn_end()

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

        for i in range(4):
            # TODO: deshacerse del turn_array y sustituirlo por un objeto para ahorrar espacio
            obj = {}
            self.game_manager.turn_manager.set_turn(self.game_manager.turn_manager.get_turn() + 1)
            self.game_manager.turn_manager.set_whose_turn_is_it(i)

            start_turn_object = self.start_turn(self.game_manager.turn_manager.get_whose_turn_is_it())
            obj['start_turn'] = start_turn_object

            commerce_phase_object = self.start_commerce_phase(self.game_manager.turn_manager.get_whose_turn_is_it(), [])
            obj['commerce_phase'] = commerce_phase_object

            build_phase_object = self.start_build_phase(self.game_manager.turn_manager.get_whose_turn_is_it(), [])
            obj['build_phase'] = build_phase_object

            print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
            print('vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv')
            end_turn_object = self.end_turn(self.game_manager.turn_manager.get_whose_turn_is_it())
            obj['end_turn'] = end_turn_object

            round_object['turn_P' + str(i)] = obj

        return round_object

    def round_end(self):
        """
        Esta función permite acabar una ronda empezada
        :return:
        """
        print('round end')
        print('---------------------')
        # if self.game_manager.turn_manager.get_round() >= 2:
        #     TODO
        # return
        # else:
        winner = False
        for player in self.game_manager.bot_manager.players:
            if player['victoryPoints'] >= 10:
                winner = True

        self.game_manager.turn_manager.set_round(self.game_manager.turn_manager.get_round() + 1)
        # if self.game_manager.turn_manager.get_round() == 2:
        #     winner = True
        return winner
        # return

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

            # self.game_manager.bot_manager.set_actual_player(i)
            # self.game_manager.turn_manager.set_whose_turn_is_it(i)
            # node_id, road_to = self.game_manager.bot_manager.players[i]['player'].on_game_start(self.game_manager.board)
            #
            # # TODO: Si no es valido,
            # #  repetir el paso "on_game_start" con el bot. En un segundo fallo directamente se le pone por él
            # print('______________________')
            # print('NODO: ' + str(node_id))
            # if self.game_manager.board.nodes[node_id]['player'] == -1:
            #     terrain_ids = self.game_manager.board.nodes[node_id]['contactingTerrain']
            #     materials = []
            #     for ter_id in terrain_ids:
            #         materials.append(self.game_manager.board.terrain[ter_id]['terrainType'])
            #     self.game_manager.board.nodes[node_id]['player'] = self.game_manager.turn_manager.get_whose_turn_is_it()
            #     print('Materiales del nodo de J' + str(self.game_manager.board.nodes[node_id]['player']))
            #     print(materials)
            #     self.game_manager.bot_manager.players[i]['player'].hand.add_material(materials, 1)
            #     self.game_manager.bot_manager.players[i]['victoryPoints'] += 1
            # else:
            #     print("el jugador " + str(self.game_manager.turn_manager.get_whose_turn_is_it()) +
            #           " ha intentado poner un nodo invalido")
            # # TODO: Si no es valido, hacer lo mismo que con el nodo, solo que mirar si se podría pedir solo la carretera
            # if (self.game_manager.board.nodes[node_id]['player']
            #         == self.game_manager.turn_manager.get_whose_turn_is_it()):
            #     response = self.game_manager.board.build_road(self.game_manager.turn_manager.get_whose_turn_is_it(),
            #                                                   node_id, road_to)
            #     if not response['response']:
            #         print(response['errorMsg'])
            #     else:
            #         setup_object["P" + str(i)].append({"id": node_id, "road": road_to})
            #     # can_build_road = True
            #     # for roads in self.game_manager.board.nodes[node_id]['roads']:
            #     #     if road_to == roads['nodeID']:
            #     #         can_build_road = False
            #     #         break
            #     #
            #     # if can_build_road:
            #     #     self.game_manager.board.nodes[node_id]['roads'].append(
            #     #         {
            #     #             "playerID": self.game_manager.turn_manager.get_whose_turn_is_it(),
            #     #             "nodeID": road_to,
            #     #         })
            #     #     print('Carretera: ')
            #     #     print(self.game_manager.board.nodes[node_id]['roads'])
            #     # else:
            #     #     print("el jugador " + str(self.game_manager.turn_manager.get_whose_turn_is_it()) +
            #     #           " ha intentado poner una carretera invalida")
            # else:
            #     print("el jugador " + str(self.game_manager.turn_manager.get_whose_turn_is_it()) +
            #           " ha intentado poner una carretera en un nodo que no le pertenece")

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

        game_object = {}
        winner = False
        while not winner:
            game_object['round_' + str(self.game_manager.turn_manager.get_round())] = self.round_start()
            winner = self.round_end()

        self.trace_loader.current_trace["setup"] = setup_object
        self.trace_loader.current_trace["game"] = game_object

        self.trace_loader.export_to_file()
        return


if __name__ == '__main__':
    print('vvvvvvvvvvvvvvvvvvvvvvvvvvvvv')
    GameDirector().game_start()
    print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
