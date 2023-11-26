class TurnManager:
    """
    Clase que se encarga de mantener la cuenta de los turnos

    En función de la fase solo se pueden hacer unas acciones u otras. La fase es 0 al inicio del turno,
    1 en el comercio, 2 en construcción y 3 en el final del turno
    """

    def __init__(self):
        self.turn, self.whose_turn_is_it, self.phase, self.round = 0, 0, 0, 0
        return

    #############################
    ########## getters ##########
    #############################
    def get_turn(self):
        """
        :return: int turn
        """
        return self.turn

    def get_whose_turn_is_it(self):
        """
        :return: int whose_turn_is_it
        """
        return self.whose_turn_is_it

    def get_phase(self):
        """
        :return: int phase
        """
        return self.phase

    def get_round(self):
        """
        :return: int round
        """
        return self.round

    #############################
    ########## setters ##########
    #############################
    def set_turn(self, turn=0):
        """
        :return: int turn
        """
        self.turn = turn
        return

    def set_whose_turn_is_it(self, player=0):
        """
        :return: int whose_turn_is_it
        """
        self.whose_turn_is_it = player
        return

    def set_phase(self, phase=0):
        """
        :return: int phase
        """
        self.phase = phase
        return

    def set_round(self, round=0):
        """
        :return: int round
        """
        self.round = round
        return
