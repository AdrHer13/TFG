from Classes.Hand import Hand
from Interfaces.BotInterface import BotInterface
from Classes.DevelopmentCards import DevelopmentCardsHand


class BotManager:
    """
    Clase que se encarga de los bots. De momento solo los carga en la partida, sin embargo cabe la posibilidad de que sea
    el bot manager el que se encargue de darle paso a los bots a hacer sus turnos
    """
    actual_player = 0
    # playerOne = BotInterface(1)
    # playerTwo = BotInterface(2)
    # playerThree = BotInterface(3)
    # playerFour = BotInterface(4)

    players = []

    # TODO: Pedir al ejecutar el programa el nombre de las clases que se quieren gastar para los bots
    # TODO: Añadir mano a self.players para que los bots puedan solicitarla pero no modificarla
    def __init__(self):
        self.players = [
            {
                'id': 0,
                'victoryPoints': 0,
                'hiddenVictoryPoints': 0,
                'player': BotInterface(0),
                'resources': Hand(),
                'development_cards': DevelopmentCardsHand(),
                'knights': 0,
                'already_played_development_card': 0,
                'largest_army': 0,
                'longest_road': 0,
            },
            {
                'id': 1,
                'victoryPoints': 0,
                'hiddenVictoryPoints': 0,
                'player': BotInterface(1),
                'resources': Hand(),
                'development_cards': DevelopmentCardsHand(),
                'knights': 0,
                'already_played_development_card': 0,
                'largest_army': 0,
                'longest_road': 0,
            },
            {
                'id': 2,
                'victoryPoints': 0,
                'hiddenVictoryPoints': 0,
                'player': BotInterface(2),
                'resources': Hand(),
                'development_cards': DevelopmentCardsHand(),
                'knights': 0,
                'already_played_development_card': 0,
                'largest_army': 0,
                'longest_road': 0,
            },
            {
                'id': 3,
                'victoryPoints': 0,
                'hiddenVictoryPoints': 0,
                'player': BotInterface(3),
                'resources': Hand(),
                'development_cards': DevelopmentCardsHand(),
                'knights': 0,
                'already_played_development_card': 0,
                'largest_army': 0,
                'longest_road': 0,
            }
        ]
        return

    def get_actual_player(self):
        return self.actual_player

    def set_actual_player(self, player_id=0):
        self.actual_player = player_id
        return
