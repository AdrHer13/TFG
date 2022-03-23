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
        # TODO: si sale un 7 deben decidir donde mover al ladrón
        print('----------')
        print('start turn: ' + str(self.game_manager.turn_manager.get_turn()))
        self.game_manager.turn_manager.set_phase(0)
        self.game_manager.bot_manager.set_actual_player(player)

        self.game_manager.throw_dice()
        self.game_manager.give_resources()

        print('Jugador: ' + str(self.game_manager.turn_manager.get_whose_turn_is_it()))
        print('Resources ActualPlayer: ' + str(self.game_manager.bot_manager.actualPlayer.hand.resources))
        print('Resources J1: ' + str(self.game_manager.bot_manager.playerOne.hand.resources))
        print('Resources J2: ' + str(self.game_manager.bot_manager.playerTwo.hand.resources))
        print('Resources J3: ' + str(self.game_manager.bot_manager.playerThree.hand.resources))
        print('Resources J4: ' + str(self.game_manager.bot_manager.playerFour.hand.resources))

        self.game_manager.bot_manager.actualPlayer.on_turn_start()
        return

    def start_commerce_phase(self, player=-1):
        """
        Esta función permite pasar a la fase de comercio
        :param player: número que representa al jugador
        :return: void
        """

        # TODO: Comprobar que el trade offer es valido. Es decir, no da más materiales de los que tiene
        print('start commerce phase: ' + str(self.game_manager.turn_manager.get_turn()))
        self.game_manager.turn_manager.set_phase(1)
        trade_offer = self.game_manager.bot_manager.actualPlayer.on_commerce_phase()
        if isinstance(trade_offer, TradeOffer):
            if trade_offer:
                print('Oferta: ' + str(trade_offer))
                # TODO: comprobar que los materiales de gives sean menores que los materiales del jugador
                if self.game_manager.bot_manager.actualPlayer.hand.resources.has_this_more_materials(trade_offer.gives):
                    print('Puede hacer la oferta')
                    self.game_manager.trade_with_everyone(trade_offer)
                else:
                    # TODO: se queja de que no puede hacerla, le da una segunda oportunidad, en otro fallo
                    #       le salta la fase de comercio
                    pass
        elif isinstance(trade_offer, dict):
            print('%%%%%%%%%%%%%%%%%%%%%%%%%%%')
            print('Jugador comercia por puerto')
            print(self.game_manager.bot_manager.actualPlayer.hand)
            response = self.game_manager.commerce_manager.trade_without_harbor(
                self.game_manager.bot_manager.actualPlayer, trade_offer['gives'], trade_offer['receives'])
            # self.game_manager.commerce_manager.trade_through_harbor(self.game_manager.bot_manager.actualPlayer,
            #                                                         trade_offer['gives'], trade_offer['receives'])
            # self.game_manager.commerce_manager.trade_through_special_harbor(self.game_manager.bot_manager.actualPlayer,
            #                                                                 trade_offer['gives'],
            #                                                                 trade_offer['receives'])
            if response:
                self.game_manager.bot_manager.actualPlayer.hand = response
                print(self.game_manager.bot_manager.actualPlayer.hand)
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
        to_build = self.game_manager.bot_manager.actualPlayer.on_build_phase(self.game_manager.board)
        if isinstance(to_build, dict):
            built = False
            if to_build['building'] == BuildConstants.TOWN:
                built = self.game_manager.build_town(self.game_manager.bot_manager.actualPlayer, to_build['nodeID'])
            elif to_build['building'] == BuildConstants.CITY:
                built = self.game_manager.build_city(self.game_manager.bot_manager.actualPlayer, to_build['nodeID'])
            elif to_build['building'] == BuildConstants.ROAD:
                built = self.game_manager.build_road(self.game_manager.bot_manager.actualPlayer, to_build['nodeID'],
                                                     to_build['roadTo'])
            elif to_build['building'] == BuildConstants.CARD:
                built = self.game_manager.build_development_card(self.game_manager.bot_manager.actualPlayer)
                # TODO
                return

            if isinstance(built, dict):
                if built['response']:
                    print('J' + str(player) + ' ha construido algo: ')
                    print(built)
                    # Si se ha construido permitir que vuelvan a construir
                    self.start_build_phase(self.game_manager.bot_manager.actualPlayer)
                else:
                    print('J' + str(player) + ' ha fallado en algo: ')
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
        self.game_manager.turn_manager.set_phase(3)
        self.game_manager.bot_manager.actualPlayer.on_turn_end()
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
        i = 1
        while i < 5:
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
        if self.game_manager.turn_manager.get_round() >= 2:
            # TODO
            return
        else:
            self.game_manager.turn_manager.set_round(self.game_manager.turn_manager.get_round() + 1)
            self.round_start()

        return

    # Game #
    def game_start(self):
        """
        Esta función permite comenzar una partida nueva
        :return:
        """
        print('game start')
        # Se cargan los bots y se inicializa el tablero
        self.game_manager.bot_manager.load_bots()
        self.game_manager.board.__init__()

        # TODO: falta comprobar que en los nodos adyacentes no hayan pueblos tampoco
        #   Falta también que se entreguen los materiales a los jugadores correspondientes
        #   Y que de alguna manera dejen de repartirse los materiales a todas las instancias de la clase en lugar de a 1
        #   Es verdad, se supone que no se pueden seleccionar casillas con puertos de buenas a primeras

        # Se le da paso al primer jugador para que ponga un poblado y una aldea
        i = 1
        while i <= 4:
            self.game_manager.bot_manager.set_actual_player(i)
            self.game_manager.turn_manager.set_whose_turn_is_it(i)
            node_id, road_to = self.game_manager.bot_manager.actualPlayer.on_game_start(self.game_manager.board)

            # TODO: Si no es valido,
            #  repetir el paso "on_game_start" con el bot. En un segundo fallo directamente se le pone por él
            print('______________________')
            print('NODO: ' + str(node_id))
            if self.game_manager.board.nodes[node_id]['player'] == 0:
                terrain_ids = self.game_manager.board.nodes[node_id]['contactingTerrain']
                materials = []
                for ter_id in terrain_ids:
                    materials.append(self.game_manager.board.terrain[ter_id]['terrainType'])
                self.game_manager.board.nodes[node_id]['player'] = self.game_manager.turn_manager.get_whose_turn_is_it()
                print('Materiales del nodo de J' + str(self.game_manager.board.nodes[node_id]['player']))
                print(materials)
                self.game_manager.bot_manager.get_player_from_int(i).hand.add_material(materials, 1)
            else:
                print("el jugador " + str(self.game_manager.turn_manager.get_whose_turn_is_it()) +
                      " ha intentado poner un nodo invalido")

            # TODO: Si no es valido, hacer lo mismo que con el nodo, solo que mirar si se podría pedir solo la carretera
            if (self.game_manager.board.nodes[node_id]['player'] ==
                    self.game_manager.turn_manager.get_whose_turn_is_it()):
                can_build_road = True
                for roads in self.game_manager.board.nodes[node_id]['roads']:
                    if road_to == roads['NodeID']:
                        can_build_road = False
                        break

                if can_build_road:
                    self.game_manager.board.nodes[node_id]['roads'].append(
                        {
                            "playerID": self.game_manager.turn_manager.get_whose_turn_is_it(),
                            "nodeID": road_to,
                        })
                else:
                    print("el jugador " + str(self.game_manager.turn_manager.get_whose_turn_is_it()) +
                          " ha intentado poner una carretera invalida")

            else:
                print("el jugador " + str(self.game_manager.turn_manager.get_whose_turn_is_it()) +
                      " ha intentado poner una carretera en un nodo que no le pertence")
            i += 1

        i = 4
        while i >= 1:
            self.game_manager.bot_manager.set_actual_player(i)
            self.game_manager.turn_manager.set_whose_turn_is_it(i)
            node_id, road_to = self.game_manager.bot_manager.actualPlayer.on_game_start(self.game_manager.board)

            # TODO: Si no es valido,
            #  repetir el paso "on_game_start" con el bot. En un segundo fallo directamente se le pone por él
            print('______________________')
            print('NODO: ' + str(node_id))
            if self.game_manager.board.nodes[node_id]['player'] == 0:
                terrain_ids = self.game_manager.board.nodes[node_id]['contactingTerrain']
                materials = []
                for ter_id in terrain_ids:
                    materials.append(self.game_manager.board.terrain[ter_id]['terrainType'])
                self.game_manager.board.nodes[node_id]['player'] = self.game_manager.turn_manager.get_whose_turn_is_it()
                print('Materiales del nodo de J' + str(self.game_manager.board.nodes[node_id]['player']))
                print(materials)
                self.game_manager.bot_manager.get_player_from_int(i).hand.add_material(materials, 1)
            else:
                print("el jugador " + str(self.game_manager.turn_manager.get_whose_turn_is_it()) +
                      " ha intentado poner un nodo invalido")
            # TODO: Si no es valido, hacer lo mismo que con el nodo, solo que mirar si se podría pedir solo la carretera
            if self.game_manager.board.nodes[node_id][
                'player'] == self.game_manager.turn_manager.get_whose_turn_is_it():
                can_build_road = True
                for roads in self.game_manager.board.nodes[node_id]['roads']:
                    if road_to == roads['nodeID']:
                        can_build_road = False
                        break

                if can_build_road:
                    self.game_manager.board.nodes[node_id]['roads'].append(
                        {
                            "playerID": self.game_manager.turn_manager.get_whose_turn_is_it(),
                            "nodeID": road_to,
                        })
                else:
                    print("el jugador " + str(self.game_manager.turn_manager.get_whose_turn_is_it()) +
                          " ha intentado poner una carretera invalida")
            else:
                print("el jugador " + str(self.game_manager.turn_manager.get_whose_turn_is_it()) +
                      " ha intentado poner una carretera en un nodo que no le pertence")
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

        self.round_start()
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
