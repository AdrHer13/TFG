from Classes.Board import Board


class LongestRoadTest:
    board = Board()

    def __init__(self):
        self.board = Board()

        self.board.nodes[0]['player'] = 0
        self.board.build_road(0, 0, 1)
        self.board.build_road(0, 1, 2)
        self.board.build_road(0, 0, 8)
        self.board.build_road(0, 8, 9)
        self.board.build_road(0, 9, 10)

        self.board.build_town(0, 10)
        self.board.build_road(0, 10, 11)
        self.board.build_road(0, 11, 21)

        self.board.build_road(0, 20, 21)
        self.board.build_road(0, 21, 22)
        self.board.build_road(0, 22, 23)
        self.board.build_town(0, 20)

        self.board.nodes[47]['player'] = 0
        self.board.build_road(0, 47, 39)

        self.board.nodes[17]['player'] = 1
        self.board.build_road(1, 17, 18)
        self.board.build_road(1, 18, 19)
        self.board.build_road(1, 19, 20)
        self.board.build_road(1, 20, 31)  # No debería de poder construirla pero deja, de momento es conveniento
        self.board.build_road(1, 31, 32)
        self.board.build_road(1, 32, 33)
        self.board.build_road(1, 33, 34)
        self.board.build_road(1, 34, 35)
        self.board.build_town(1, 35)
        self.board.build_road(1, 35, 24)
        self.board.build_road(1, 24, 25)
        self.board.build_road(1, 25, 26)
        self.board.build_road(1, 26, 37)
        self.board.build_road(1, 36, 37)  # Si está activo este, gana J2, si no gana J1. Algoritmo va

        self.board.build_road(1, 33, 22)
        # self.board.build_road(1, 26, 37)

    def longest_road_calculator(self, node, depth, longest_road_obj, player_id, visited_nodes=None):
        """
        :param node:
        :param depth:
        :param longest_road:
        :param visited_nodes:
        :return:
        """
        if visited_nodes is None:
            visited_nodes = []

        for road in node['roads']:
            # print('. . . . . . . ')
            # print('Road to: ' + str(road['nodeID']))
            if ((road['nodeID'] not in visited_nodes) and
                (road['playerID'] == player_id or player_id == -1) and
                (road['playerID'] == node['player'] or node['player'] == -1)):
                visited_nodes.append(road['nodeID'])
                # print(visited_nodes)
                # print(node)
                if depth > longest_road_obj['longest_road']:
                    longest_road_obj['longest_road'] = depth
                    longest_road_obj['player'] = player_id
                # print('depth: ' + str(depth))
                # print('player: ' + str(player_id))
                longest_road_obj = self.longest_road_calculator(self.board.nodes[road['nodeID']], depth + 1, longest_road_obj, road['playerID'], visited_nodes)
        return {'longest_road': longest_road_obj['longest_road'], 'player': longest_road_obj['player']}

    def longest_road_test(self):
        # for node in self.board.nodes:
        #     self.longest_road_calculator(node, 0, [])

        real_longest_road = {'longest_road': 5, 'player': -1}
        for node in self.board.nodes:
            longest_road_obj = self.longest_road_calculator(node, 1, {'longest_road': 0, 'player': -1}, -1, [node['id']])
            print('. . . . . . . . .')
            print('Node start: ' + str(node['id']))
            print('Longer:')
            print(longest_road_obj)
            if longest_road_obj['longest_road'] > real_longest_road['longest_road']:
                real_longest_road = longest_road_obj

        print('-- -- -- -- -- -- -- -- --')
        print('Longest: ')
        print(real_longest_road)

        #     for road in node['roads']:
        #         if road['nodeID'] not in visited_nodes:
        #             visited_nodes.append(road['nodeID'])
        #
        #             for road_2 in self.board.nodes[road['nodeID']]:
        #                 if road_2['nodeID'] not in visited_nodes:
        #                     visited_nodes.append(road['nodeID'])
        # pass


if __name__ == '__main__':
    test = LongestRoadTest()
    test.longest_road_test()
    # test.board.visualize_board()
