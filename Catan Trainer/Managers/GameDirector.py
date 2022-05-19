import random

from Classes.Constants import BuildConstants
from Classes.TradeOffer import TradeOffer
from Managers.GameManager import GameManager


class GameDirector:
    """
    Clase que se encarga de dirigir la partida, empezarla y acabarla
    """
    # turn_manager = TurnManager()
    # bot_manager = BotManager()
    game_manager = GameManager()

    def __init__(self):
        return

    # Turn #
    def start_turn(self, player=-1):
        """
        Esta función permite iniciar el turno
        :param player: número que representa al jugador
        :return: void
        """
        print('----------')
        print('start turn: ' + str(self.game_manager.turn_manager.get_turn()))
        self.game_manager.turn_manager.set_phase(0)
        self.game_manager.bot_manager.set_actual_player(player)

        self.game_manager.throw_dice()
        self.game_manager.give_resources()
        # self.game_manager.give_all_resources()

        print('Jugador: ' + str(self.game_manager.turn_manager.get_whose_turn_is_it()))
        # print('Resources ActualPlayer: ' + str(self.game_manager.bot_manager.players[player]['player'].hand.resources))
        print('Resources J0: ' + str(self.game_manager.bot_manager.players[0]['player'].hand.resources) + ' | Total: ' + str(self.game_manager.bot_manager.players[0]['player'].hand.get_total()))
        print('Resources J1: ' + str(self.game_manager.bot_manager.players[1]['player'].hand.resources) + ' | Total: ' + str(self.game_manager.bot_manager.players[1]['player'].hand.get_total()))
        print('Resources J2: ' + str(self.game_manager.bot_manager.players[2]['player'].hand.resources) + ' | Total: ' + str(self.game_manager.bot_manager.players[2]['player'].hand.get_total()))
        print('Resources J3: ' + str(self.game_manager.bot_manager.players[3]['player'].hand.resources) + ' | Total: ' + str(self.game_manager.bot_manager.players[3]['player'].hand.get_total()))

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

            print('Jugador: ' + str(self.game_manager.turn_manager.get_whose_turn_is_it()))
            # print('Resources ActualPlayer: ' + str(
            #     self.game_manager.bot_manager.players[player]['player'].hand.resources))
            print('Resources J0: ' + str(self.game_manager.bot_manager.players[0]['player'].hand.resources) + ' | Total: ' + str(self.game_manager.bot_manager.players[0]['player'].hand.get_total()))
            print('Resources J1: ' + str(self.game_manager.bot_manager.players[1]['player'].hand.resources) + ' | Total: ' + str(self.game_manager.bot_manager.players[1]['player'].hand.get_total()))
            print('Resources J2: ' + str(self.game_manager.bot_manager.players[2]['player'].hand.resources) + ' | Total: ' + str(self.game_manager.bot_manager.players[2]['player'].hand.get_total()))
            print('Resources J3: ' + str(self.game_manager.bot_manager.players[3]['player'].hand.resources) + ' | Total: ' + str(self.game_manager.bot_manager.players[3]['player'].hand.get_total()))

            on_moving_thief = self.game_manager.bot_manager.players[player]['player'].on_moving_thief()
            self.game_manager.move_thief(on_moving_thief['terrain'], on_moving_thief['player'])

        # LLama al inicio del turno de los jugadores
        # self.game_manager.bot_manager.players[player]['player'].on_turn_start()
        return

    def start_commerce_phase(self, player=-1):
        """
        Esta función permite pasar a la fase de comercio
        :param player: número que representa al jugador
        :return: void
        """
        # TODO: Comprobar que el trade offer es valido. Es decir, no da más materiales de los que tiene
        print('Start commerce phase: ' + str(self.game_manager.turn_manager.get_turn()))
        self.game_manager.turn_manager.set_phase(1)
        trade_offer = self.game_manager.bot_manager.players[player]['player'].on_commerce_phase()
        if isinstance(trade_offer, TradeOffer):
            if trade_offer:
                print('Oferta: ' + str(trade_offer))
                # TODO: comprobar que los materiales de gives sean menores que los materiales del jugador
                if self.game_manager.bot_manager.players[player]['player'].hand.resources.has_this_more_materials(
                        trade_offer.gives):
                    print('Puede hacer la oferta')
                    self.game_manager.trade_with_everyone(trade_offer)
                else:
                    # TODO: se queja de que no puede hacerla, le da una segunda oportunidad, en otro fallo
                    #       le salta la fase de comercio
                    pass
        elif isinstance(trade_offer, dict):
            print('%%%%%%%%%%%%%%%%%%%%%%%%%%%')
            print('Jugador comercia por puerto')
            print(self.game_manager.bot_manager.players[player]['player'].hand)
            response = self.game_manager.commerce_manager.trade_without_harbor(
                self.game_manager.bot_manager.players[player]['player'], trade_offer['gives'], trade_offer['receives'])
            # self.game_manager.commerce_manager.trade_through_harbor(self.game_manager.bot_manager.actualPlayer,
            #                                                         trade_offer['gives'], trade_offer['receives'])
            # self.game_manager.commerce_manager.trade_through_special_harbor(self.game_manager.bot_manager.actualPlayer,
            #                                                                 trade_offer['gives'],
            #                                                                 trade_offer['receives'])
            if response:
                self.game_manager.bot_manager.players[player]['player'].hand = response
                print(self.game_manager.bot_manager.players[player]['player'].hand)
            else:
                print('pero no tiene materiales suficientes')
            print('%%%%%%%%%%%%%%%%%%%%%%%%%%%')
            return
        else:
            return

    def start_build_phase(self, player=-1):
        """
        Esta función permite pasar a la fase de construcción
        :param player: número que representa al jugador
        :return: void
        """
        print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
        print('vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv')
        print('start build phase: ' + str(self.game_manager.turn_manager.get_turn()))
        self.game_manager.turn_manager.set_phase(2)
        to_build = self.game_manager.bot_manager.players[player]['player'].on_build_phase(self.game_manager.board)
        if isinstance(to_build, dict):
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
                return

            if isinstance(built, dict):
                if built['response']:
                    print('J' + str(player) + ' ha construido algo: ')
                    print(to_build)
                    # Si se ha construido permitir que vuelvan a construir
                    self.start_build_phase(player)
                else:
                    print('J' + str(player) + ' ha fallado en algo: ')
                    print(to_build)
                    print(built['errorMsg'])
                    # TODO: Avisar que no se ha podido construir
                    return
            else:
                print('No se ha podido construir por falta de materiales')
                # TODO: Avisar que no se ha podido construir
                return
        else:
            return

    def end_turn(self, player=-1):
        """
        Esta función permite finalizar el turno
        :param player: número que representa al jugador
        :return: void
        """
        print('start end turn: ' + str(self.game_manager.turn_manager.get_turn()))
        print('----- Puntos de victoria de los jugadores: ------')
        for i in range(4):
            print('J' + str(i) + ': ' + str(self.game_manager.bot_manager.players[i]['victoryPoints']))
        print('----- FIN Puntos de victoria de los jugadores ------')
        self.game_manager.turn_manager.set_phase(3)
        self.game_manager.bot_manager.players[player]['player'].on_turn_end()
        self.game_manager.graphics_manager.flip()
        return

    # def end_phase(self):
    #     # TODO
    #     # Probablemente innecesario
    #     print('end phase')
    #     if self.game_manager.turn_manager.phase == 0:
    #         self.start_commerce_phase(self.game_manager.turn_manager.get_whose_turn_is_it())
    #     elif self.game_manager.turn_manager.phase == 1:
    #         self.start_build_phase(self.game_manager.turn_manager.get_whose_turn_is_it())
    #     elif self.game_manager.turn_manager.phase == 2:
    #         self.end_turn(self.game_manager.turn_manager.get_whose_turn_is_it())
    #     elif self.game_manager.turn_manager.phase == 3:
    #         if self.game_manager.turn_manager.get_whose_turn_is_it() >= 4:
    #             self.round_end()
    #         else:
    #             self.game_manager.turn_manager.set_whose_turn_is_it(
    #                 self.game_manager.turn_manager.get_whose_turn_is_it() + 1)
    #             self.start_turn(self.game_manager.turn_manager.whoseTurnIsIt)
    #     else:
    #         pass
    #     return

    # Round #
    def round_start(self):
        """
        Esta función permite comenzar una ronda nueva
        :return:
        """
        print('---------------------')
        print('round start')
        i = 0
        while i < 4:
            self.game_manager.turn_manager.set_turn(self.game_manager.turn_manager.get_turn() + 1)
            self.game_manager.turn_manager.set_whose_turn_is_it(i)

            self.start_turn(self.game_manager.turn_manager.get_whose_turn_is_it())
            self.start_commerce_phase(self.game_manager.turn_manager.get_whose_turn_is_it())
            self.start_build_phase(self.game_manager.turn_manager.get_whose_turn_is_it())
            print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
            print('vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv')
            self.end_turn(self.game_manager.turn_manager.get_whose_turn_is_it())
            i += 1
        self.round_end()
        return

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

        # TODO: falta comprobar que en los nodos adyacentes no hayan pueblos tampoco
        #   Y que de alguna manera dejen de repartirse los materiales a todas las instancias de la clase en lugar de a 1
        #   Es verdad, se supone que no se pueden seleccionar casillas con puertos de buenas a primeras

        # Se le da paso al primer jugador para que ponga un poblado y una aldea
        i = 0
        while i <= 3:
            self.game_manager.bot_manager.set_actual_player(i)
            self.game_manager.turn_manager.set_whose_turn_is_it(i)
            node_id, road_to = self.game_manager.bot_manager.players[i]['player'].on_game_start(self.game_manager.board)

            # TODO: Si no es valido,
            #  repetir el paso "on_game_start" con el bot. En un segundo fallo directamente se le pone por él
            print('______________________')
            print('NODO: ' + str(node_id))
            if self.game_manager.board.nodes[node_id]['player'] == -1:
                terrain_ids = self.game_manager.board.nodes[node_id]['contactingTerrain']
                materials = []
                for ter_id in terrain_ids:
                    materials.append(self.game_manager.board.terrain[ter_id]['terrainType'])
                self.game_manager.board.nodes[node_id]['player'] = self.game_manager.turn_manager.get_whose_turn_is_it()
                print('Materiales del nodo de J' + str(self.game_manager.board.nodes[node_id]['player']))
                print(materials)
                self.game_manager.bot_manager.players[i]['player'].hand.add_material(materials, 1)
                self.game_manager.bot_manager.players[i]['victoryPoints'] += 1
            else:
                print("el jugador " + str(self.game_manager.turn_manager.get_whose_turn_is_it()) +
                      " ha intentado poner un nodo invalido")

            # TODO: Si no es valido, hacer lo mismo que con el nodo, solo que mirar si se podría pedir solo la carretera
            if (self.game_manager.board.nodes[node_id]['player'] ==
                    self.game_manager.turn_manager.get_whose_turn_is_it()):
                response = self.game_manager.board.build_road(self.game_manager.turn_manager.get_whose_turn_is_it(),
                                                              node_id, road_to)
                if not response['response']:
                    print(response['errorMsg'])
                # can_build_road = True
                # for roads in self.game_manager.board.nodes[node_id]['roads']:
                #     if road_to == roads['nodeID']:
                #         can_build_road = False
                #         break
                #
                # if can_build_road:
                #     self.game_manager.board.nodes[node_id]['roads'].append(
                #         {
                #             "playerID": self.game_manager.turn_manager.get_whose_turn_is_it(),
                #             "nodeID": road_to,
                #         })
                #     print('Carretera: ')
                #     print(self.game_manager.board.nodes[node_id]['roads'])
                # else:
                #     print("el jugador " + str(self.game_manager.turn_manager.get_whose_turn_is_it()) +
                #           " ha intentado poner una carretera invalida")

            else:
                print("el jugador " + str(self.game_manager.turn_manager.get_whose_turn_is_it()) +
                      " ha intentado poner una carretera en un nodo que no le pertence")
            i += 1

        i = 3
        while i >= 0:
            self.game_manager.bot_manager.set_actual_player(i)
            self.game_manager.turn_manager.set_whose_turn_is_it(i)
            node_id, road_to = self.game_manager.bot_manager.players[i]['player'].on_game_start(self.game_manager.board)

            # TODO: Si no es valido,
            #  repetir el paso "on_game_start" con el bot. En un segundo fallo directamente se le pone por él
            print('______________________')
            print('NODO: ' + str(node_id))
            if self.game_manager.board.nodes[node_id]['player'] == -1:
                terrain_ids = self.game_manager.board.nodes[node_id]['contactingTerrain']
                materials = []
                for ter_id in terrain_ids:
                    materials.append(self.game_manager.board.terrain[ter_id]['terrainType'])
                self.game_manager.board.nodes[node_id]['player'] = self.game_manager.turn_manager.get_whose_turn_is_it()
                print('Materiales del nodo de J' + str(self.game_manager.board.nodes[node_id]['player']))
                print(materials)
                self.game_manager.bot_manager.players[i]['player'].hand.add_material(materials, 1)
                self.game_manager.bot_manager.players[i]['victoryPoints'] += 1
            else:
                print("el jugador " + str(self.game_manager.turn_manager.get_whose_turn_is_it()) +
                      " ha intentado poner un nodo invalido")
            # TODO: Si no es valido, hacer lo mismo que con el nodo, solo que mirar si se podría pedir solo la carretera
            if (self.game_manager.board.nodes[node_id]['player']
                    == self.game_manager.turn_manager.get_whose_turn_is_it()):
                response = self.game_manager.board.build_road(self.game_manager.turn_manager.get_whose_turn_is_it(),
                                                              node_id, road_to)
                if not response['response']:
                    print(response['errorMsg'])
                # can_build_road = True
                # for roads in self.game_manager.board.nodes[node_id]['roads']:
                #     if road_to == roads['nodeID']:
                #         can_build_road = False
                #         break
                #
                # if can_build_road:
                #     self.game_manager.board.nodes[node_id]['roads'].append(
                #         {
                #             "playerID": self.game_manager.turn_manager.get_whose_turn_is_it(),
                #             "nodeID": road_to,
                #         })
                #     print('Carretera: ')
                #     print(self.game_manager.board.nodes[node_id]['roads'])
                # else:
                #     print("el jugador " + str(self.game_manager.turn_manager.get_whose_turn_is_it()) +
                #           " ha intentado poner una carretera invalida")
            else:
                print("el jugador " + str(self.game_manager.turn_manager.get_whose_turn_is_it()) +
                      " ha intentado poner una carretera en un nodo que no le pertenece")
            i -= 1

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

        winner = False
        while not winner:
            self.round_start()
            winner = self.round_end()
        return

    def game_end(self):
        """
        Esta función permite acabar una partida empezada
        :return:
        """
        print('game end')
        return

    def check_for_victory(self):
        """
        Esta función comprueba si alguno de los 4 jugadores ha conseguido la condición de victoria
        :return:
        """
        print('check for victory')
        return


if __name__ == '__main__':
    print('vvvvvvvvvvvvvvvvvvvvvvvvvvvvv')
    GameDirector().game_start()
    print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
