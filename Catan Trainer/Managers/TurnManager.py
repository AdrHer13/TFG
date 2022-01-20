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
        return

    #############################
    ########## getters ##########
    #############################
    def get_turn(self):
        """
        :return: int turn
        """
        return

    def get_whose_turn_is_it(self):
        """
        :return: int whose_turn_is_it
        """
        return

    def get_phase(self):
        """
        :return: int phase
        """
        return

    def get_round(self):
        """
        :return: int round
        """
        return
