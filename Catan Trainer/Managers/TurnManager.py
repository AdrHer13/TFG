class TurnManager:
    """
    Clase que se encarga de mantener la cuenta de los turnos

    En función de la fase solo se pueden hacer unas acciones u otras. La fase es 0 al inicio del turno,
    1 en el comercio, 2 en construcción y 3 en el final del turno
    """

    turn = int
    whoseTurnIsIt = int
    phase = int
    round = int

    def __init__(self):
        self.turn, self.whoseTurnIsIt, self.phase, self.round = 0, 1, 0, 0
        return

    def end_phase(self):
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
        return self.whoseTurnIsIt

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
    def set_turn(self, turn=int):
        """
        :return: int turn
        """
        self.turn = turn
        return

    def set_whose_turn_is_it(self, player=int):
        """
        :return: int whose_turn_is_it
        """
        self.whoseTurnIsIt = player
        return

    def set_phase(self, phase=int):
        """
        :return: int phase
        """
        self.phase = phase
        return

    def set_round(self, round=int):
        """
        :return: int round
        """
        self.round = round
        return
