#
# Clase que se encarga de dirigir una partida de Catan
#
import random

from Classes.Board import Board
from Classes.Constants import MaterialConstants
from Classes.TradeOffer import TradeOffer
from Managers.TurnManager import TurnManager
from Managers.CommerceManager import CommerceManager
from Managers.BotManager import BotManager


class GameManager:
    """
    Clase que representa el game manager, entidad que tiene todas las acciones que pueden hacer los jugadores
    """
    last_dice_roll = 0
    board = Board()
    turn_manager = TurnManager()
    commerce_manager = CommerceManager()
    bot_manager = BotManager()

    def __init__(self):
        return

    def throw_dice(self):
        """
        Función que devuelve un valor entre el 2 y el 12, simulando una tirada de 2d6
        :return: integer entre 2 y 12
        """
        self.last_dice_roll = random.randint(2, 12)
        print('throw dice: ' + str(self.last_dice_roll))
        return

    def give_resources(self):
        """
        Función que entrega materiales a cada uno de los jugadores en función de la tirada de dados
        :return: void
        """
        # Por cada pieza de terreno en el tablero
        for terrain in self.board.terrain:
            # Si la probabilidad coincide
            if terrain['probability'] == self.last_dice_roll:
                # Se miran los nodos adyacentes
                for node in terrain['contactingNodes']:
                    # Si tiene jugador, implica que hay pueblo
                    if self.board.nodes[node]['player'] != 0:
                        player = self.bot_manager.get_player_from_int(self.board.nodes[node]['player'])
                        # Si tiene ciudad se dan 2 en lugar de 1 material

                        if self.board.nodes[node]['hasCity']:
                            print('J' + str(self.board.nodes[node]['player']) + ' | material: ' + str(
                                terrain['terrainType']) + ' | amount: 2')
                            player.hand.add_material(terrain['terrainType'], 2)
                        else:
                            print('J' + str(self.board.nodes[node]['player']) + ' | material: ' + str(
                                terrain['terrainType']) + ' | amount: 1')
                            player.hand.add_material(terrain['terrainType'], 1)
        return None

    def trade_with_everyone(self, trade_offer=TradeOffer()):
        """
        Permite enviar una oferta a todos los jugadores en la mesa. Si alguno acepta se hará el intercambio
        :param trade_offer: Oferta de comercio con el jugador, debe incluir qué se entrega y qué se recibe
        :return: void
        """

        receivers = self.bot_manager.get_other_players_except_int(self.turn_manager.whoseTurnIsIt)
        giver = self.bot_manager.get_player_from_int(self.turn_manager.whoseTurnIsIt)
        for receiver in receivers:
            response = receiver.on_trade_offer(trade_offer)

            if isinstance(response, TradeOffer):
                # TODO: usar recursividad o una función externa que pueda usarse recursivamente para establecer limites
                #       arbitrarios
                print('J' + str(receiver.id) + ' ofrece contraoferta')
                print('Contraoferta: ' + str(response))
                response_from_giver = giver.on_trade_offer(response)
                if isinstance(response_from_giver, TradeOffer):
                    # response_from_giver = False
                    response_from_giver = True
                if response_from_giver:
                    print('J' + str(giver.id) + ' ha aceptado')
                    done = self.trade_with_player(response, receiver, giver)
                    if done:
                        return
                else:
                    print('J' + str(giver.id) + ' ha negado')
            else:
                # En caso de que no haya contraoferta, o han aceptado o han denegado.
                if response:
                    print('J' + str(receiver.id) + ' ha aceptado')
                    done = self.trade_with_player(trade_offer, giver, receiver)
                    if done:
                        return
                else:
                    print('J' + str(receiver.id) + ' ha denegado')
        return

    def trade_with_player(self, trade_offer=None, giver=None, receiver=None):
        """
        Función que hace el intercambio entre dos jugadores
        :param trade_offer: TradeOffer()
        :param giver: BotInterface()
        :param receiver: BotInterface()
        :return: bool
        """
        if trade_offer is None or giver is None or receiver is None:
            return False

        # Si receiver o giver no tiene materiales se le ignora
        if (receiver.hand.resources.has_this_more_materials(trade_offer.receives) and
                giver.hand.resources.has_this_more_materials(trade_offer.gives)):
            print('Puede hacerse el intercambio: ')
            # Se hace el intercambio

            print('Giver: ' + str(giver.hand))
            print('Receiver: ' + str(receiver.hand))
            # Se resta lo que da del giver
            giver.hand.remove_material(MaterialConstants.WOOL, trade_offer.gives.wool)
            giver.hand.remove_material(MaterialConstants.WOOD, trade_offer.gives.wood)
            giver.hand.remove_material(MaterialConstants.CLAY, trade_offer.gives.clay)
            giver.hand.remove_material(MaterialConstants.CEREAL, trade_offer.gives.cereal)
            giver.hand.remove_material(MaterialConstants.MINERAL, trade_offer.gives.mineral)

            # Se añade lo que recibe
            giver.hand.add_material(MaterialConstants.WOOL, trade_offer.receives.wool)
            giver.hand.add_material(MaterialConstants.WOOD, trade_offer.receives.wood)
            giver.hand.add_material(MaterialConstants.CLAY, trade_offer.receives.clay)
            giver.hand.add_material(MaterialConstants.CEREAL, trade_offer.receives.cereal)
            giver.hand.add_material(MaterialConstants.MINERAL, trade_offer.receives.mineral)

            # Se resta lo que receiver entrega
            receiver.hand.remove_material(MaterialConstants.WOOL, trade_offer.receives.wool)
            receiver.hand.remove_material(MaterialConstants.WOOD, trade_offer.receives.wood)
            receiver.hand.remove_material(MaterialConstants.CLAY, trade_offer.receives.clay)
            receiver.hand.remove_material(MaterialConstants.CEREAL, trade_offer.receives.cereal)
            receiver.hand.remove_material(MaterialConstants.MINERAL, trade_offer.receives.mineral)

            # Se añade lo que receiver recibe
            receiver.hand.add_material(MaterialConstants.WOOL, trade_offer.gives.wool)
            receiver.hand.add_material(MaterialConstants.WOOD, trade_offer.gives.wood)
            receiver.hand.add_material(MaterialConstants.CLAY, trade_offer.gives.clay)
            receiver.hand.add_material(MaterialConstants.CEREAL, trade_offer.gives.cereal)
            receiver.hand.add_material(MaterialConstants.MINERAL, trade_offer.gives.mineral)

            print('-------------------------')
            print('Giver: ' + str(giver.hand))
            print('Receiver: ' + str(receiver.hand))
            return True
        else:
            print('No tienen materiales suficientes para completar la oferta')
            return False

    ########### Board functions ###################
    def build_town(self, player, node):
        """
        Permite construir un pueblo en el nodo seleccionado
        :param player: Número que representa al jugador
        :param node: Número que representa un nodo en el tablero
        :return: void
        """
        return self.board.build_town(player, node)

    def build_city(self, player, node):
        """
        Permite construir una ciudad en el nodo seleccionado
        :param player: Número que representa al jugador
        :param node: Número que representa un nodo en el tablero
        :return: void
        """
        return self.board.build_city(player, node)

    def build_road(self, player, road):
        """
        Permite construir una carretera en el camino seleccionado
        :param player: Número que representa al jugador
        :param road: Número que representa una carretera en el tablero
        :return: void
        """
        # self.board.build_road(player, road)
        return

    def move_thief(self, terrain, adjacentPlayer):
        """
        Permite mover al ladrón a la casilla de terreno seleccionada y en caso de que haya un poblado o ciudad de otro
        jugador adyacente a dicha casilla permite robarle un material aleatorio de la mano.
        :param terrain: Número que representa un hexágono en el tablero
        :param adjacentPlayer: Número de un jugador que esté adyacente al hexágono seleccionado
        :return: void
        """
        # self.board.move_thief(terrain)
        self.__steal_from_player__(adjacentPlayer)
        return

    def __steal_from_player__(self, player):
        """
        Función que permite robar de manera aleatoria un material de la mano de un jugador.
        :param player: Número que representa a un jugador
        :return: void
        """
        pass
