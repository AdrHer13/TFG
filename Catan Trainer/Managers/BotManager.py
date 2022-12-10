from pydoc import locate

from Bots import RandomBot
from Classes.Hand import Hand
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
        first_bot_class = self.import_bot_class_from_input('primer')
        second_bot_class = self.import_bot_class_from_input('segundo')
        third_bot_class = self.import_bot_class_from_input('tercer')
        fourth_bot_class = self.import_bot_class_from_input('cuarto')

        self.players = [
            {
                'id': 0,
                'victory_points': 0,
                'hidden_victory_points': 0,
                'player': first_bot_class(0),
                'resources': Hand(),
                'development_cards': DevelopmentCardsHand(),
                'knights': 0,
                'already_played_development_card': 0,
                'largest_army': 0,
                'longest_road': 0,
            },
            {
                'id': 1,
                'victory_points': 0,
                'hidden_victory_points': 0,
                'player': second_bot_class(1),
                'resources': Hand(),
                'development_cards': DevelopmentCardsHand(),
                'knights': 0,
                'already_played_development_card': 0,
                'largest_army': 0,
                'longest_road': 0,
            },
            {
                'id': 2,
                'victory_points': 0,
                'hidden_victory_points': 0,
                'player': third_bot_class(2),
                'resources': Hand(),
                'development_cards': DevelopmentCardsHand(),
                'knights': 0,
                'already_played_development_card': 0,
                'largest_army': 0,
                'longest_road': 0,
            },
            {
                'id': 3,
                'victory_points': 0,
                'hidden_victory_points': 0,
                'player': fourth_bot_class(3),
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

    def import_bot_class_from_input(self, strng=''):
        module_class = input('Módulo y clase del ' + strng + ' bot (ej: mymodule.myclass)(dejar en blanco para usar la por defecto): ')
        if module_class == '':
            klass = RandomBot.RandomBot
        else:
            components = module_class.split('.')
            module = __import__('Bots.' + components[0], fromlist=[components[1]])
            klass = getattr(module, components[1])

        return klass
