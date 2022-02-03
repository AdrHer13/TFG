from Managers.GameManager import GameManager


class Interpreter:
    game_manager = GameManager()

    def __init__(self):
        return

    """
    La idea es que el interprete coja el JSON y lo permita reproducir. Habría que pensarlo más a fondo, si el interprete
    sirve también como reproductor, pasar de turno o de ronda o mostrarlo todo de golpe en ASCII medianamente legible 
    """