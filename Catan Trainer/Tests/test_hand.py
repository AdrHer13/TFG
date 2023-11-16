from Classes.Constants import MaterialConstants as mc
from Classes.Hand import *


class TestHand:
    def test_hand_materials(self):
        hand = Hand()

        # Comprobamos que la mano empieza sin materiales
        assert hand.get_total() == 0

        # Comprobamos que add_material añade materiales correctamente
        hand.add_material(mc.CEREAL, 1)
        hand.add_material(mc.MINERAL, 1)
        hand.add_material(mc.CLAY, 1)
        hand.add_material(mc.WOOD, 1)
        hand.add_material(mc.WOOL, 1)
        assert hand.get_cereal() == 1 and hand.get_mineral() == 1 and hand.get_clay() == 1 and hand.get_wood() == 1 and \
               hand.get_wool() == 1 and hand.get_total() == 5

        # Comprobamos que la versión por lista funciona correctamente también
        hand.add_material([0, 1, 2, 3, 4], 1)
        assert hand.get_cereal() == 2 and hand.get_mineral() == 2 and hand.get_clay() == 2 and hand.get_wood() == 2 and \
               hand.get_wool() == 2 and hand.get_total() == 10

        # Comprobamos que remove_material elimina materiales correctamente
        hand.remove_material(0, 1)
        hand.remove_material(1, 1)
        hand.remove_material(2, 1)
        hand.remove_material(3, 1)
        hand.remove_material(4, 1)
        assert hand.get_cereal() == 1 and hand.get_mineral() == 1 and hand.get_clay() == 1 and hand.get_wood() == 1 and \
               hand.get_wool() == 1 and hand.get_total() == 5

        # Comprobamos que la versión por lista funciona correctamente también
        hand.remove_material([0, 1, 2, 3, 4], 1)
        assert hand.get_total() == 0

        # Comprobamos si se lanza la excepción al tener menos materiales de los posibles
        assert hand.remove_material(0, 1) == False
        # Comprobamos qué pasa si se resta 0
        assert hand.remove_material(0, 0) == True

        # Comprobamos qué pasa si se elimina un material pese a tener al menos 1
        hand.add_material(0, 1)
        assert hand.remove_material(0, 1) == True

        return
