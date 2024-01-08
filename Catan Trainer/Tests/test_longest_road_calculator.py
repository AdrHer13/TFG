from Managers.GameManager import *


class TestLongestRoadCalculator:
    def longest_road_test(self):
        gm = GameManager(for_test=True)
        longest_road = {'longest_road': 4, 'player': -1}

        for case in range(4):
            if case == 0:  # Caso 1: Aún no hay nadie con 5 o más caminos
                gm.board.nodes[0]['player'] = 0
                gm.board.build_road(0, 0, 1)
                gm.board.build_road(0, 1, 2)
                gm.board.build_road(0, 0, 8)

            if case == 1:  # Caso 2: Hay un jugador con 5 o más caminos
                gm.board.build_road(0, 8, 9)
                gm.board.build_road(0, 9, 10)

            if case == 2:  # Caso 3: Otro jugador tiene igual cantidad de caminos que el que poseía el camino más largo
                gm.board.nodes[17]['player'] = 1
                gm.board.build_road(1, 17, 18)
                gm.board.build_road(1, 18, 19)
                gm.board.build_road(1, 19, 20)
                gm.board.build_road(1, 20, 31)
                gm.board.build_road(1, 31, 32)

            if case == 3:  # Caso 4: Otro jugador tiene más caminos que el que poseía el camino más largo
                gm.board.build_road(1, 32, 33)
                gm.board.build_road(1, 33, 34)
                gm.board.build_road(1, 34, 35)

            for node in gm.board.nodes:
                longest_road_obj = gm.longest_road_calculator(node, 1, longest_road, -1, [node['id']])

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


if __name__ == '__main__':
    test = TestLongestRoadCalculator()
    test.longest_road_test()
