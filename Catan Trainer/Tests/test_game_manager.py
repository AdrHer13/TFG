from Managers.GameManager import GameManager
from Classes.Materials import Materials
from Classes.TradeOffer import TradeOffer
from Classes.Constants import MaterialConstants, DevelopmentCardConstants


class TestGameManager:
    game_manager = GameManager(for_test=True)

    def test_reset_values(self):
        self.game_manager.already_played_development_card = True
        self.game_manager.last_dice_roll = 4
        self.game_manager.largest_army = 5
        self.game_manager.largest_army_player = {"name": "<NAME>"}
        self.game_manager.longest_road = {"name": "<NAME>"}
        self.game_manager.board.build_town(0, 0)
        self.game_manager.board.build_city(0, 0)
        self.game_manager.board.build_town(2, 7)
        self.game_manager.development_cards_deck.draw_card()
        self.game_manager.set_turn(2)
        self.game_manager.set_whose_turn_is_it(3)
        self.game_manager.set_phase(1)
        self.game_manager.set_round(10)
        self.game_manager.bot_manager.players[0]['victory_points'] = 5

        self.game_manager.reset_game_values()

        assert self.game_manager.already_played_development_card is False
        assert self.game_manager.last_dice_roll == 0
        assert self.game_manager.largest_army_player == {} and self.game_manager.largest_army == 2
        assert self.game_manager.longest_road == {'longest_road': 4, 'player': -1}
        assert (self.game_manager.board.nodes[0]['player'] == -1 and
                self.game_manager.board.nodes[0]['has_city'] is False)
        assert (self.game_manager.board.nodes[0]['player'] == -1 and
                self.game_manager.board.nodes[0]['has_city'] is False)
        assert (self.game_manager.board.nodes[2]['player'] == -1 and
                self.game_manager.board.nodes[7]['has_city'] is False)
        assert (self.game_manager.development_cards_deck.deck != [] and
                self.game_manager.development_cards_deck.current_index == 0)
        assert (self.game_manager.turn_manager.turn == 0 and self.game_manager.turn_manager.whose_turn_is_it == 0 and
                self.game_manager.turn_manager.phase == 0 and self.game_manager.turn_manager.round == 0)
        assert self.game_manager.bot_manager.players[0]['victory_points'] == 0

    def test_give_resources(self):
        self.game_manager.reset_game_values()

        self.game_manager.last_dice_roll = 11
        # Añadimos pueblos al J0
        self.game_manager.board.nodes[20]['player'] = 0  # Un pueblo adyacente
        self.game_manager.board.nodes[13]['player'] = 0  # Un pueblo no adyacente
        self.game_manager.board.nodes[33]['player'] = 0
        self.game_manager.board.build_city(0, 33)  # Una ciudad adyacente

        # Añadimos pueblos al J2
        self.game_manager.board.nodes[10]['player'] = 2  # Un pueblo adyacente
        self.game_manager.board.nodes[39]['player'] = 2  # Un pueblo no adyacente
        self.game_manager.board.nodes[0]['player'] = 2
        self.game_manager.board.build_city(2, 0)  # Una ciudad adyacente

        self.game_manager.give_resources()

        # Comprobamos los del J0
        assert self.game_manager.bot_manager.players[0]['player'].hand.resources.get_cereal() == 3
        assert self.game_manager.bot_manager.players[0]['resources'].resources.get_cereal() == 3

        assert self.game_manager.bot_manager.players[0]['player'].hand.resources.get_mineral() == 0
        assert self.game_manager.bot_manager.players[0]['resources'].resources.get_mineral() == 0

        assert self.game_manager.bot_manager.players[0]['player'].hand.resources.get_clay() == 0
        assert self.game_manager.bot_manager.players[0]['resources'].resources.get_clay() == 0

        assert self.game_manager.bot_manager.players[0]['player'].hand.resources.get_wood() == 0
        assert self.game_manager.bot_manager.players[0]['resources'].resources.get_wood() == 0

        assert self.game_manager.bot_manager.players[0]['player'].hand.resources.get_wool() == 0
        assert self.game_manager.bot_manager.players[0]['resources'].resources.get_wool() == 0

        # Comprobamos los del J2
        assert self.game_manager.bot_manager.players[2]['player'].hand.resources.get_cereal() == 0
        assert self.game_manager.bot_manager.players[2]['resources'].resources.get_cereal() == 0

        assert self.game_manager.bot_manager.players[2]['player'].hand.resources.get_mineral() == 0
        assert self.game_manager.bot_manager.players[2]['resources'].resources.get_mineral() == 0

        assert self.game_manager.bot_manager.players[2]['player'].hand.resources.get_clay() == 0
        assert self.game_manager.bot_manager.players[2]['resources'].resources.get_clay() == 0

        assert self.game_manager.bot_manager.players[2]['player'].hand.resources.get_wood() == 3
        assert self.game_manager.bot_manager.players[2]['resources'].resources.get_wood() == 3

        assert self.game_manager.bot_manager.players[2]['player'].hand.resources.get_wool() == 0
        assert self.game_manager.bot_manager.players[2]['resources'].resources.get_wool() == 0

    def test_send_trade_to_everyone(self):
        trade = TradeOffer(Materials(1, 0, 0, 0, 0), Materials(0, 0, 1, 0, 1))

        assert type(self.game_manager.send_trade_to_everyone(trade)) is list

    def test__on_tradeoffer_response(self):
        return

    def test__trade_with_player(self):
        self.game_manager.reset_game_values()

        self.game_manager._give_all_resources()

        response = self.game_manager._trade_with_player()

        assert response is False

        trade_offer = TradeOffer(gives=Materials(1, 0, 0, 0, 0), receives=Materials(0, 0, 1, 1, 0))
        giver = self.game_manager.bot_manager.players[0]
        receiver = self.game_manager.bot_manager.players[2]

        response = self.game_manager._trade_with_player(trade_offer, giver, receiver)

        assert response is True
        assert self.game_manager.bot_manager.players[0]['resources'].get_total() == 26
        assert self.game_manager.bot_manager.players[2]['resources'].get_total() == 24

    def test_build_road(self):
        self.game_manager.reset_game_values()

        # No tenemos materiales suficientes así que no hará nada
        assert self.game_manager.build_road(0, 0, 1)['response'] is False

        self.game_manager.bot_manager.players[0]['resources'].add_material([MaterialConstants.CLAY,
                                                                            MaterialConstants.WOOD
                                                                            ], 1)
        # No tenemos poblado así que no hará nada
        assert self.game_manager.build_road(0, 0, 1)['response'] is False

        self.game_manager.board.nodes[0]['player'] = 0

        assert self.game_manager.build_road(0, 0, 1)['response'] is True
        assert self.game_manager.bot_manager.players[0]['resources'].get_total() == 0

    def test_build_town(self):
        self.game_manager.reset_game_values()

        # No tenemos materiales suficientes así que no hará nada
        assert self.game_manager.build_town(0, 0)['response'] is False

        self.game_manager.bot_manager.players[0]['resources'].add_material([MaterialConstants.CEREAL,
                                                                            MaterialConstants.CLAY,
                                                                            MaterialConstants.WOOD,
                                                                            MaterialConstants.WOOL
                                                                            ], 1)
        # No tenemos carretera así que no hará nada
        assert self.game_manager.build_town(0, 0)['response'] is False

        self.game_manager.board.nodes[0]['roads'].append({'player_id': 0, 'node_id': 1})

        assert self.game_manager.build_town(0, 0)['response'] is True
        assert self.game_manager.bot_manager.players[0]['resources'].get_total() == 0

    def test_build_city(self):
        self.game_manager.reset_game_values()

        # No tenemos materiales suficientes así que no hará nada
        assert self.game_manager.build_city(0, 0)['response'] is False

        self.game_manager.bot_manager.players[0]['resources'].add_material([MaterialConstants.CEREAL,
                                                                            MaterialConstants.MINERAL
                                                                            ], 3)
        # No tenemos poblado así que no hará nada
        assert self.game_manager.build_city(0, 0)['response'] is False

        self.game_manager.board.nodes[0]['player'] = 0

        assert self.game_manager.build_city(0, 0)['response'] is True
        assert self.game_manager.bot_manager.players[0]['resources'].get_total() == 1

    def test_build_development_card(self):
        self.game_manager.reset_game_values()

        # No tenemos materiales suficientes así que no hará nada
        assert self.game_manager.build_development_card(0)['response'] is False

        self.game_manager.bot_manager.players[0]['resources'].add_material([MaterialConstants.CEREAL,
                                                                            MaterialConstants.MINERAL,
                                                                            MaterialConstants.WOOL
                                                                            ], 1)

        assert self.game_manager.build_development_card(0)['response'] is True
        assert self.game_manager.bot_manager.players[0]['resources'].get_total() == 0

        self.game_manager.development_cards_deck.current_index = 25
        # No quedan más cartas que robar
        assert self.game_manager.build_development_card(0)['response'] is False

    def test_move_thief(self):
        self.game_manager.reset_game_values()

        self.game_manager.board.nodes[0]['player'] = 0
        self.game_manager.board.nodes[32]['player'] = 3

        self.game_manager.bot_manager.players[3]['resources'].add_material([MaterialConstants.CEREAL,
                                                                            MaterialConstants.MINERAL,
                                                                            MaterialConstants.WOOL
                                                                            ], 1)
        self.game_manager.move_thief(9, 3)
        assert self.game_manager.bot_manager.players[0]['resources'].get_total() == 1
        assert self.game_manager.bot_manager.players[3]['resources'].get_total() == 2

    def test__steal_from_player(self):
        self.game_manager.reset_game_values()
        self.game_manager.bot_manager.actual_player = 0

        self.game_manager._give_all_resources()

        material = self.game_manager._steal_from_player(1)

        assert self.game_manager.bot_manager.players[0]['resources'].get_total() == 26
        assert self.game_manager.bot_manager.players[1]['resources'].get_total() == 24
        assert self.game_manager.bot_manager.players[0]['resources'].get_from_id(material) == 6
        assert self.game_manager.bot_manager.players[1]['resources'].get_from_id(material) == 4

    def test_on_game_start_build_towns_and_roads(self):
        self.game_manager.reset_game_values()

        valid_nodes = self.game_manager.board.valid_starting_nodes()

        node, road = self.game_manager.on_game_start_build_towns_and_roads(0)

        assert node in valid_nodes
        assert road in self.game_manager.board.nodes[node]['adjacent']

    def test_longest_road(self):
        self.game_manager.reset_game_values()
        longest_road = {'longest_road': 4, 'player': -1}

        for case in range(4):
            if case == 0:  # Caso 1: Aún no hay nadie con 5 o más caminos
                self.game_manager.board.nodes[0]['player'] = 0
                self.game_manager.board.build_road(0, 0, 1)
                self.game_manager.board.build_road(0, 1, 2)
                self.game_manager.board.build_road(0, 0, 8)

            if case == 1:  # Caso 2: Hay un jugador con 5 o más caminos
                self.game_manager.board.build_road(0, 8, 9)
                self.game_manager.board.build_road(0, 9, 10)

            if case == 2:  # Caso 3: Otro jugador tiene igual cantidad de caminos que el que poseía el camino más largo
                self.game_manager.board.nodes[17]['player'] = 1
                self.game_manager.board.build_road(1, 17, 18)
                self.game_manager.board.build_road(1, 18, 19)
                self.game_manager.board.build_road(1, 19, 20)
                self.game_manager.board.build_road(1, 20, 31)
                self.game_manager.board.build_road(1, 31, 32)

            if case == 3:  # Caso 4: Otro jugador tiene más caminos que el que poseía el camino más largo
                self.game_manager.board.build_road(1, 32, 33)
                self.game_manager.board.build_road(1, 33, 34)
                self.game_manager.board.build_road(1, 34, 35)

            for node in self.game_manager.board.nodes:
                longest_road_obj = self.game_manager.longest_road_calculator(node, 1, longest_road, -1, [node['id']])

                if longest_road_obj['longest_road'] >= longest_road['longest_road']:
                    longest_road = longest_road_obj

            if case == 0:  # Caso 1: Aún no hay nadie con 5 o más caminos
                assert longest_road == {'longest_road': 4, 'player': -1}

            if case == 1:  # Caso 2: Hay un jugador con 5 o más caminos
                assert longest_road == {'longest_road': 5, 'player': 0}

            if case == 2:  # Caso 3: Otro jugador alcanza la misma cantidad de caminos que el que tiene la carretera
                assert longest_road == {'longest_road': 5, 'player': 0}

            if case == 3:  # Caso 4: Otro jugador tiene más caminos que el que poseía el camino más largo
                assert longest_road == {'longest_road': 8, 'player': 1}
        return

    def test_play_development_card(self):
        done_0 = True
        done_1 = True
        done_1_1 = True
        done_2 = True
        done_2_2 = False
        done_2_2_1 = True
        done_2_3 = False
        done_2_4 = False
        winner = False

        while done_0 or done_1 or done_2:
            self.game_manager.reset_game_values()

            self.game_manager.board.nodes[24]['player'] = 0
            self.game_manager.board.nodes[19]['player'] = 1
            self.game_manager.board.nodes[42]['player'] = 2
            self.game_manager.board.nodes[0]['player'] = 3
            for player in range(3):
                self.game_manager.bot_manager.players[player]['resources'].add_material([MaterialConstants.CEREAL,
                                                                                         MaterialConstants.MINERAL,
                                                                                         MaterialConstants.CLAY,
                                                                                         MaterialConstants.WOOL,
                                                                                         MaterialConstants.WOOD
                                                                                         ], 1)

            self.game_manager.bot_manager.players[3]['resources'].add_material([MaterialConstants.CEREAL,
                                                                                MaterialConstants.MINERAL,
                                                                                MaterialConstants.WOOL,
                                                                                ], 1)
            self.game_manager.build_development_card(3)
            card = self.game_manager.bot_manager.players[3]['development_cards'].hand[
                len(self.game_manager.bot_manager.players[3]['development_cards'].hand) - 1]

            if card.get_type() == DevelopmentCardConstants.KNIGHT and done_0:
                card, winner = self.game_manager.play_development_card(3, card, winner)

                assert winner is False
                assert self.game_manager.bot_manager.players[3]['knights'] == 1
                done_0 = False

            elif card.get_type() == DevelopmentCardConstants.VICTORY_POINT and done_1:
                if done_1_1:
                    self.game_manager.bot_manager.players[3]['victory_points'] = 9
                    card, winner = self.game_manager.play_development_card(3, card, winner)

                    assert winner is True
                    assert card['played_card'] == 'victory_point'

                    winner = False
                    done_1_1 = False

                else:
                    card, winner = self.game_manager.play_development_card(3, card, winner)

                    assert winner is False
                    assert card['played_card'] == 'failed_victory_point'
                    done_1 = False

            elif card.get_type() == DevelopmentCardConstants.PROGRESS_CARD and done_2:

                if card.get_effect() == DevelopmentCardConstants.MONOPOLY_EFFECT and not done_2_4:
                    card, winner = self.game_manager.play_development_card(3, card, winner)

                    assert winner is False
                    assert card['played_card'] == 'monopoly'
                    assert self.game_manager.bot_manager.players[3]['resources'].get_total() == 3
                    assert self.game_manager.bot_manager.players[1]['resources'].get_from_id(
                        card['material_chosen']) == 0
                    done_2_4 = True

                elif card.get_effect() == DevelopmentCardConstants.ROAD_BUILDING_EFFECT and not done_2_2:
                    if done_2_2_1:
                        card_bad, winner = self.game_manager.play_development_card(3, card, winner)

                        assert winner is False
                        assert card_bad['roads'] is None
                        done_2_2_1 = False
                    else:
                        # self.game_manager.board.build_road(3, 0, 1)
                        card, winner = self.game_manager.play_development_card(3, card, winner)  # Auxilio no se porqué no vaaaaaaaaaaaaaaaaaaaaaa

                        assert winner is False
                        print(card['roads'])
                        # assert card['roads'] is dict
                        assert card['played_card'] == 'road_building'

                        done_2_2 = True

                elif card.get_effect() == DevelopmentCardConstants.YEAR_OF_PLENTY_EFFECT and not done_2_3:
                    card, winner = self.game_manager.play_development_card(3, card, winner)

                    assert winner is False
                    assert card['played_card'] == 'year_of_plenty'
                    assert self.game_manager.bot_manager.players[3]['resources'].get_total() == 2
                    done_2_3 = True

                elif done_2_4 and done_2_3 and done_2_2:
                    done_2 = False

    def test_check_if_thief_is_called(self):
        self.game_manager.reset_game_values()

        self.game_manager.last_dice_roll = 7
        self.game_manager.board.nodes[24]['player'] = 0
        self.game_manager.board.nodes[19]['player'] = 1
        self.game_manager.board.nodes[42]['player'] = 2
        self.game_manager.board.nodes[0]['player'] = 3

        for player in range(4):
            self.game_manager.bot_manager.players[player]['resources'].add_material([MaterialConstants.CEREAL,
                                                                                     MaterialConstants.MINERAL,
                                                                                     MaterialConstants.CLAY,
                                                                                     MaterialConstants.WOOL,
                                                                                     MaterialConstants.WOOD
                                                                                     ], player)
            self.game_manager.bot_manager.players[player]['player'].hand = (
                self.game_manager.bot_manager.players)[player]['resources']

        start_turn_object = {}
        start_turn_object = self.game_manager.check_if_thief_is_called(start_turn_object, 2)

        assert start_turn_object['past_thief_terrain'] != start_turn_object['thief_terrain']

        assert self.game_manager.bot_manager.players[0]['resources'].get_total() == 0
        assert self.game_manager.bot_manager.players[1]['resources'].get_total() == 5
        assert self.game_manager.bot_manager.players[2]['resources'].get_total() == 5
        assert self.game_manager.bot_manager.players[3]['resources'].get_total() == 7

    def test_on_commerce_response(self):
        return

    def test_build_phase_object(self):
        return


if __name__ == '__main__':
    test = TestGameManager()
    # test.test_reset_values()
    # test.test_give_resources()
    # test.test_send_trade_to_everyone()   #########
    # test.test__on_tradeoffer_response()  #########
    # test.test__trade_with_player()
    # test.test_build_town()
    # test.test_build_city()
    # test.test_build_road()
    # test.test_build_development_card()
    # test.test_move_thief()
    # test.test__steal_from_player()
    # test.test_game_start_build_towns_and_roads()
    # test.test_longest_road()
    # test.test_play_development_card()
    # test.test_check_if_thief_is_called()
    # test.test_on_commerce_response()     #########
    # test.test_build_phase_object()       #########
