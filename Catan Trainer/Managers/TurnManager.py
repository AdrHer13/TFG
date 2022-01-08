#
# Clase que se encarga de mantener la cuenta de los turnos
#
#
# En función de la fase solo se pueden hacer unas acciones u otras. La fase es 0 al inicio del turno,
# 1 en el comercio, 2 en construcción y 3 en el final del turno
#
class TurnManager:
    turn = int
    whoseTurnIsIt = int
    phase = int

    # init()
    def __init__(self):
        return

    # start_turn() -> void
    #
    # Esta función permite iniciar el turno
    def start_turn(self):
        return

    # start_commerce_phase() -> void
    #
    # Esta función permite pasar a la fase de comercio
    def start_commerce_phase(self):
        return

    # start_build_phase() -> void
    #
    # Esta función permite pasar a la fase de construcción
    def start_build_phase(self):
        return

    # end_turn() -> void
    #
    # Esta función permite finalizar el turno
    def end_turn(self):
        return

    #############################
    ########## getters ##########
    #############################
    # get_turn() -> int turn
    def get_turn(self):
        return

    # get_whose_turn_is_it() -> int whoseTurnIsIt
    def get_whose_turn_is_it(self):
        return

    # get_phase() -> int phase
    def get_phase(self):
        return

