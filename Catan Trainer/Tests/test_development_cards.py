from Classes.Constants import *
from Classes.DevelopmentCards import *


class TestDevelopmentCards:
    Dcc = DevelopmentCardConstants

    def test_development_deck(self):
        development_deck = DevelopmentDeck()
        # Comprobamos que el deck se compone de 15 caballeros, 5 puntos de victoria y 2 de cada carta especial
        for card in development_deck.deck:
            if 0 <= card.id < 14:
                assert card.get_effect() == Dcc.KNIGHT_EFFECT and card.get_type() == Dcc.KNIGHT
            elif 14 <= card.id < 19:
                assert card.get_effect() == Dcc.VICTORY_POINT_EFFECT and card.get_type() == Dcc.VICTORY_POINT
            elif 19 <= card.id < 21:
                assert card.get_effect() == Dcc.ROAD_BUILDING_EFFECT and card.get_type() == Dcc.PROGRESS_CARD
            elif 21 <= card.id < 23:
                assert card.get_effect() == Dcc.YEAR_OF_PLENTY_EFFECT and card.get_type() == Dcc.PROGRESS_CARD
            elif 23 <= card.id < 25:
                assert card.get_effect() == Dcc.MONOPOLY_EFFECT and card.get_type() == Dcc.PROGRESS_CARD

        # Se comprueba que se baraja la baraja
        initial_values = []
        for card in development_deck.deck:
            initial_values.append(card)

        development_deck.shuffle_deck()
        assert initial_values != development_deck.deck

        # Se comprueba que draw_card() devuelve la primera carta del deck y si se roba una segunda carta, no es la misma
        first_card_in_deck = development_deck.deck[0]
        drawn_card = development_deck.draw_card()
        assert first_card_in_deck.get_id() == drawn_card.get_id()

        second_drawn_card = development_deck.draw_card()
        assert drawn_card.get_id() != second_drawn_card.get_id()
        return

    def test_development_cards_hand(self):
        development_deck = DevelopmentDeck()
        # development_deck.shuffle_deck()
        hand_of_cards = DevelopmentCardsHand()

        # Vemos que la mano no posee cartas
        assert len(hand_of_cards.hand) == 0

        # Añadimos una carta a la mano y miramos que tiene al menos 1 carta
        hand_of_cards.add_card(development_deck.draw_card())
        assert len(hand_of_cards.hand) == 1

        # Añadimos algo que no sea una carta y comprobamos que no se añade
        hand_of_cards.add_card('string to see that it doesn\'t get added')
        hand_of_cards.add_card(None)
        assert len(hand_of_cards.hand) == 1

        # Comprobamos que check_hand() devuelve la mano en diccionarios y no en objetos DevelopmentCard()
        hand_dictionary = hand_of_cards.check_hand()
        assert hand_dictionary == [{'id': 0, 'type': Dcc.KNIGHT, 'effect': Dcc.KNIGHT_EFFECT}]

        # Robamos 2 cartas más para simular una mano mayor a 1 carta
        hand_of_cards.add_card(development_deck.draw_card())
        hand_of_cards.add_card(development_deck.draw_card())

        # Comprobamos que se pueden jugar cartas. El game_manager es el encargado de borrarlas de la mano
        played_card = hand_of_cards.play_card_by_id(2)
        assert played_card.get_id() == 2 and played_card.get_effect() == Dcc.KNIGHT_EFFECT and played_card.get_type() == Dcc.KNIGHT

        played_card = hand_of_cards.play_card_by_array_index(0)
        assert played_card.get_id() == 0 and played_card.get_effect() == Dcc.KNIGHT_EFFECT and played_card.get_type() == Dcc.KNIGHT

        # Comprobamos que la función delete_card() borra la carta correctamente por ID
        hand_of_cards.delete_card(1)
        assert hand_of_cards.check_hand() == [{'id': 0, 'type': Dcc.KNIGHT, 'effect': Dcc.KNIGHT_EFFECT},
                                              {'id': 2, 'type': Dcc.KNIGHT, 'effect': Dcc.KNIGHT_EFFECT}]
        return
