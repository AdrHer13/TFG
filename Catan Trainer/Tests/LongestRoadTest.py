from Managers.GameManager import *


class LongestRoadTest:
    def longest_road_test(self):
        gm = GameManager(for_test=True)

        gm.board.nodes[0]['player'] = 0
        gm.board.build_road(0, 0, 1)
        gm.board.build_road(0, 1, 2)
        gm.board.build_road(0, 0, 8)
        gm.board.build_road(0, 8, 9)
        gm.board.build_road(0, 9, 10)

        gm.board.build_town(0, 10)
        gm.board.build_road(0, 10, 11)
        gm.board.build_road(0, 11, 21)

        gm.board.build_road(0, 20, 21)
        gm.board.build_road(0, 21, 22)
        gm.board.build_road(0, 22, 23)
        gm.board.build_town(0, 20)

        gm.board.nodes[47]['player'] = 0
        gm.board.build_road(0, 47, 39)

        gm.board.nodes[17]['player'] = 1
        gm.board.build_road(1, 17, 18)
        gm.board.build_road(1, 18, 19)
        gm.board.build_road(1, 19, 20)
        gm.board.build_road(1, 20, 31)  # No debería de poder construirla, pero deja, de momento es conveniento
        gm.board.build_road(1, 31, 32)
        gm.board.build_road(1, 32, 33)
        gm.board.build_road(1, 33, 34)
        gm.board.build_road(1, 34, 35)
        gm.board.build_town(1, 35)
        gm.board.build_road(1, 35, 24)
        gm.board.build_road(1, 24, 25)
        gm.board.build_road(1, 25, 26)
        gm.board.build_road(1, 26, 37)
        gm.board.build_road(1, 36, 37)  # Si está activo este, gana J2, si no gana J1. Algoritmo va

        gm.board.build_road(1, 33, 22)

        real_longest_road = {'longest_road': 5, 'player': -1}
        for node in gm.board.nodes:
            longest_road_obj = gm.longest_road_calculator(node, 1, {'longest_road': 0, 'player': -1}, -1, [node['id']])

            if longest_road_obj['longest_road'] > real_longest_road['longest_road']:
                real_longest_road = longest_road_obj
        return


if __name__ == '__main__':
    test = LongestRoadTest()
    test.longest_road_test()
