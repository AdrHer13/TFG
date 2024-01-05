class TurnManager:
    """
    Clase que se encarga de mantener la cuenta de los turnos

    En función de la fase solo se pueden hacer unas acciones u otras. La fase es 0 al inicio del turno,
    1 en el comercio, 2 en construcción y 3 en el final del turno
    """

    def __init__(self, turn=0, whose_turn_is_it=0, phase=0, round=0):
        self.turn = turn
        self.whose_turn_is_it = whose_turn_is_it
        self.phase = phase
        self.round = round
        return

    # -- -- -- --  getters  -- -- -- --
    def get_turn(self):
        """
        :return: turn: int
        """
        return self.turn

    def get_whose_turn_is_it(self):
        """
        :return: whose_turn_is_it: int
        """
        return self.whose_turn_is_it

    def get_phase(self):
        """
        :return: phase: int
        """
        return self.phase

    def get_round(self):
        """
        :return: round: int
        """
        return self.round

    # -- -- -- --  setters  -- -- -- --
    def set_turn(self, turn=0):
        """
        :param turn: int
        :return:
        """
        self.turn = turn
        return

    def set_whose_turn_is_it(self, player=0):
        """
        :param player: int
        :return:
        """
        self.whose_turn_is_it = player
        return

    def set_phase(self, phase=0):
        """
        :param phase: int
        :return:
        """
        self.phase = phase
        return

    def set_round(self, round=0):
        """
        :param round: int
        :return:
        """
        self.round = round
        return
