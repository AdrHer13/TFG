from Classes.Board import Board
from Managers.BotManager import BotManager
from Managers.GameManager import GameManager


class TestGameManager:
    game_manager = GameManager(True)
    init_board = Board()

    def test_game_manager_reset_values(self):
        self.game_manager.reset_game_values()
        assert self.game_manager.last_dice_roll == 0
        assert self.game_manager.board.nodes == self.init_board.nodes and self.game_manager.board.terrain == self.init_board.terrain
        assert self.game_manager.development_cards_deck.deck != [] and self.game_manager.development_cards_deck.current_index == 0
        assert self.game_manager.turn_manager.turn == 0 and self.game_manager.turn_manager.whose_turn_is_it == 0 and \
               self.game_manager.turn_manager.phase == 0 and self.game_manager.turn_manager.round == 0
        assert self.game_manager.commerce_manager != ''
        assert self.game_manager.bot_manager.players != []
        assert self.game_manager.largest_army_player == {} and self.game_manager.largest_army == 2

    def test_game_manager_give_resources(self):
        # TODO: Hay que definir un estado de tablero controlable.
        #  Forzar una tirada específica.
        #  Ver que se entregan los materiales bien
        self.game_manager.board.build_town()

        self.game_manager.give_resources()
