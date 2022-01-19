class TurnManager:
    """
    Clase que se encarga de mantener la cuenta de los turnos

    En función de la fase solo se pueden hacer unas acciones u otras. La fase es 0 al inicio del turno,
    1 en el comercio, 2 en construcción y 3 en el final del turno
    """

    turn = int
    whoseTurnIsIt = int
    phase = int

    def __init__(self):
        return

    def start_turn(self):
        """
        Esta función permite iniciar el turno
        :return: void
        """
        return

    def start_commerce_phase(self):
        """
        Esta función permite pasar a la fase de comercio
        :return: void
        """
        return

    def start_build_phase(self):
        """
        Esta función permite pasar a la fase de construcción
        :return: void
        """
        return

    def end_turn(self):
        """
        Esta función permite finalizar el turno
        :return: void
        """
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
