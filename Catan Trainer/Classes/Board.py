#
# Clase que representa una instancia del tablero.
#
class Board:
    nodes = []
    roads = []
    origTerrain = []
    terrain = []
    terrainProb = []

    # init()
    #
    # Cuando se llama al init se establece el valor inicial del tablero antes de que se pongan pueblos y carreteras.
    # Aquí se pone el terreno y su probabilidad
    def __init__(self):
        return

    # build_town(player, node) -> void
    #
    # Permite construir un pueblo por el jugador especificado en el cruce escrito
    # Cambia la variable nodes para colocar un pueblo en ello
    def build_town(self, player, node):
        return

    # build_city(player, node) -> void
    #
    # Permite construir una ciudad por el jugador especificado en el cruce escrito
    # Cambia la variable nodes para colocar una ciudad en ello
    def build_city(self, player, node):
        return

    # build_road(player, road) -> void
    #
    # Permite construir una carretera por el jugador especificado en la carretera especificada
    # Cambia la variable roads para colocar una carretera del jugador designado en ella
    def build_road(self, player, road):
        return

    # move_thief(terrain) -> void
    #
    # Permite mover el ladron a la casilla de terreno especificada
    # Cambia la variable terrain para colocar al ladron en el terreno correspondiente
    def move_thief(self, terrain):
        return

    # update_board() -> void
    #
    # Actualiza visualmente el tablero con todos los cambios habidos desde el último update
    def update_board(self):
        return
