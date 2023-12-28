import math
import random

from Classes.Constants import DevelopmentCardConstants as Dcc


# Debido a como funciona el juego, en caso de querer lanzar una carta de desarrollo debería de lanzarse siempre que un jugador devuelva
#  una carta como parte de su on_... Si devuelve una carta, el GameManager resuelve su efecto y cuenta cualquier otra carta que intente lanzar
#  como un paso de fase.
class DevelopmentDeck:
    # Solo puedes JUGAR una carta desarrollo (comprar las que sean)
    # Sin embargo, puedes jugar cualquier cantidad de cartas de desarrollo que otorguen puntos de victoria
    # Las cartas que dan puntos de victoria (idealmente) se mantienen en secreto del resto de jugadores hasta que puedas ganar con ello
    # NO puedes jugar una carta que acabas de comprar
    # A MENOS que sea una que te lleve a 10 puntos de victoria
    # Se pueden jugar en cualquier momento de una ronda, incluso antes de tirar el dado (en cualquier on_... del bot)

    deck = []  # Deck es un array de objetos carta
    current_index = 0  # La carta que se va a robar si alguien construye una

    def __init__(self):
        # Se vacía primero por completo el deck para evitar que se dupliquen las cartas
        self.deck.clear()
        # Genera el array de cartas de desarrollo y lo baraja
        # Hay 14 soldados
        # 6 cartas de progreso (2 de cada)
        # 5 de puntos de victoria
        for i in range(0, 14):
            self.deck.append(DevelopmentCard(i, Dcc.KNIGHT, Dcc.KNIGHT_EFFECT))
        for i in range(14, 19):
            self.deck.append(DevelopmentCard(i, Dcc.VICTORY_POINT, Dcc.VICTORY_POINT_EFFECT))
        for i in range(19, 21):
            self.deck.append(DevelopmentCard(i, Dcc.PROGRESS_CARD, Dcc.ROAD_BUILDING_EFFECT))
        for i in range(21, 23):
            self.deck.append(DevelopmentCard(i, Dcc.PROGRESS_CARD, Dcc.YEAR_OF_PLENTY_EFFECT))
        for i in range(23, 25):
            self.deck.append(DevelopmentCard(i, Dcc.PROGRESS_CARD, Dcc.MONOPOLY_EFFECT))
        return

    def shuffle_deck(self):
        # Se barajan las cartas de desarrollo
        current_index, random_index = len(self.deck), 0
        while current_index != 0:
            random_index = math.floor(random.random() * current_index)
            current_index -= 1
            (self.deck[current_index], self.deck[random_index]) = (self.deck[random_index], self.deck[current_index])
        return

    def draw_card(self):
        if self.current_index == len(self.deck):  # No quedan cartas que robar
            pass
        else:
            card = self.deck[self.current_index]
            self.current_index += 1
            return card

    def __str__(self):
        string = '[ \n'
        for card in self.deck:
            string += card.__str__()
            string += ', \n'
        string += ']'

        return string


class DevelopmentCard:
    """
    Carta de desarrollo
    :param id: Número que identifica la carta.
    :param type: Punto de victoria, soldado, o carta de progreso (monopolio, año de la cosecha,
    construir 2 carreteras gratis).
    :param effect: En función del número que tiene, hace una cosa u otra.
    """

    def __init__(self, id=0, type='', effect=0):
        self.id = id
        self.type = type
        self.effect = effect
        pass

    def __str__(self):
        return "{'id': " + str(self.id) + ", 'type': " + str(self.type) + ", 'effect': " + str(self.effect) + "}"

    def get_id(self):
        return self.id

    def get_type(self):
        return self.type

    def get_effect(self):
        return self.effect

    def __to_object__(self):
        return {'id': self.get_id(), 'type': self.get_type(), 'effect': self.get_effect()}


class DevelopmentCardsHand:
    """
    Clase que muestra qué cartas tienes en la mano. Cada jugador solo puede ver su propia mano hasta que la juegan,
    momento en el que el efecto de la carta ocurre y cada jugador puede voluntariamente hacer un seguimiento de qué ha salido.
    """
    hand = []  # Cartas que posee en mano

    def __init__(self):
        self.hand = []
        pass

    def add_card(self, card):
        if isinstance(card, DevelopmentCard):
            self.hand.append(card)
        else:
            return

    def check_hand(self):
        """
        Devuelve la mano que tiene el jugador, por si quiere por su cuenta comprobar qué cartas posee para gastar.
        :return:
        """
        hand_array = []
        for card in self.hand:
            card_obj = {'id': card.get_id(), 'type': card.get_type(), 'effect': card.get_effect()}
            hand_array.append(card_obj)

        return hand_array

    def play_card_by_array_index(self, index):
        """
        Al usar esta función indicas que quieres jugar esta carta pasando el índice de la carta en el array,
        lo que se la pasa al gameManager y la borra de la mano.
        :param index:
        :return:
        """
        if len(self.hand):
            card_obj = self.hand[index]
            # self.delete_card(self.hand[index].id)
            return card_obj
        # print('no tenía esa carta en mano id ' + str(id))
        pass

    def play_card_by_id(self, id):
        """
        Juega la carta con el ID que se le pase, la pasa al gameManager y la borra de la mano.
        :param id: (int) Número indicativo de la carta.
        """
        for card in self.hand:
            if card.get_id() == id:
                # print('se juega carta con id ' + str(id))
                card_obj = card
                # self.delete_card(id)
                return card_obj
        # print('no tenía esa carta en mano id ' + str(id))
        pass

    def delete_card(self, id):
        """
        Borra la carta con la ID que se le pase.
        :param id: (int) Número indicativo de la carta.
        """
        # print('borra carta de mano')
        rest_of_hand = []
        # Borra la carta que con la id correcta de la mano
        for card in self.hand:
            if card.get_id() != id:
                rest_of_hand.append(card)
        self.hand = rest_of_hand
        pass


if __name__ == '__main__':
    deck = DevelopmentDeck()
    deck.shuffle_deck()
    hand = DevelopmentCardsHand()
    hand_2 = DevelopmentCardsHand()

    while True:
        hand.add_card(deck.draw_card())
        hand_2.add_card(deck.draw_card())
        print('--------------------------')
        print(hand.check_hand())
        print('##########################')
        print(hand_2.check_hand())
        # hand.play_card_by_array_index(0)
    # hand.play_card_by_id(0)
    # print(hand.check_hand())
