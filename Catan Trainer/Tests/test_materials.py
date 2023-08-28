from Classes.Constants import BuildConstants as bc
from Classes.Hand import *


class TestMaterials:
    def test_add_materials(self):
        materials = Materials()

        materials.add_mineral(1)
        assert materials.get_mineral() == 1

        materials.add_wool(2)
        assert materials.get_wool() == 2

        materials.add_wood(3)
        assert materials.get_wood() == 3

        materials.add_clay(4)
        assert materials.get_clay() == 4

        materials.add_cereal(5)
        assert materials.get_cereal() == 5

    def test_has_more_materials_than_build_values(self):
        # Comprobamos que el mínimo funciona correctamente
        materials_for_town = Materials(1, 0, 1, 1, 1)
        assert materials_for_town.has_this_more_materials(bc.TOWN)

        materials_for_city = Materials(2, 3, 0, 0, 0)
        assert materials_for_city.has_this_more_materials(bc.CITY)

        materials_for_road = Materials(0, 0, 1, 1, 0)
        assert materials_for_road.has_this_more_materials(bc.ROAD)

        materials_for_card = Materials(1, 0, 0, 1, 1)
        assert materials_for_card.has_this_more_materials(bc.CARD)

        # Comprobamos que falla correctamente también
        assert not materials_for_town.has_this_more_materials(bc.CITY)

        # Y también que funciona si se tiene materiales suficientes
        assert materials_for_town.has_this_more_materials(bc.ROAD)

        # Y debería de tener materiales suficientes
        materials = Materials(1, 0, 4, 2, 7)
        assert materials.has_this_more_materials(bc.TOWN)
