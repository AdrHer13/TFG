class Materials:
    """
    Clase que representa los materiales. Se usa tanto en la mano de los jugadores como en las ofertas
    """
    cereal = 0
    mineral = 0
    clay = 0
    wood = 0
    wool = 0

    def __init__(self):
        return

    ##### getters #####
    def get_cereal(self):
        return self.cereal

    def get_mineral(self):
        return self.mineral

    def get_clay(self):
        return self.clay

    def get_wood(self):
        return self.wood

    def get_wool(self):
        return self.wool

    ##### setters #####
    def set_cereal(self, amount=int):
        self.cereal = amount
        return

    def set_mineral(self, amount=int):
        self.mineral = amount
        return

    def set_clay(self, amount=int):
        self.clay = amount
        return

    def set_wood(self, amount=int):
        self.wood = amount
        return

    def set_wool(self, amount=int):
        self.wool = amount
        return

    ##### adders #####
    def add_cereal(self, amount):
        cereal = self.get_cereal() + amount
        self.set_cereal(cereal)
        return

    def add_mineral(self, amount):
        mineral = self.get_mineral() + amount
        self.set_mineral(mineral)
        return

    def add_clay(self, amount):
        clay = self.get_clay() + amount
        self.set_clay(clay)
        return

    def add_wood(self, amount):
        wood = self.get_wood() + amount
        self.set_wood(wood)
        return

    def add_wool(self, amount):
        wool = self.get_wool() + amount
        self.set_wool(wool)
        return
