import set_pathes

import unittest
from momo.model import MoMoModel
from momo.prototype import Prototype
from momo.system_models.system_models import MultiSystemModel, SystemModel


class TestMoMoModel(unittest.TestCase):
    def setUp(self):
        dbms = SystemModel("DBMS")
        dbms.add_feature("Security", {"MySQL": 1, "MS SQL": 1, "Oracle": 1})
        dbms.add_feature("Performance", [1, 1, 1])
        dbms.add_feature("Speed", [0, 1, 1])

        connector = SystemModel("Connector")
        connector.add_feature("Flexibility", {"Copper": 1, "Aluminum": 1})
        connector.add_feature("Cost", {"Copper": 1, "Aluminum": 1})

        self.multy_system = MultiSystemModel([dbms, connector])
        self.model = MoMoModel(self.multy_system)


    def test_init(self):
        self.assertEqual(self.model._u, 0)
        self.assertDictEqual(self.model.system_models.systems, self.multy_system.systems)
        self.assertTrue(self.model.prototype.equals(self.multy_system.get_prototype()))


    def test_init_model_incorect_system_models(self):
        with self.assertRaises(ValueError):
            MoMoModel([1, 2, 3])


    def test_init_model_incorect_prototype(self):
        with self.assertRaises(ValueError):
            MoMoModel(self.multy_system, 1)


    def test_init_model_incorect_meanshure_of_prototype(self):
        with self.assertRaises(ValueError):
            MoMoModel(self.multy_system, Prototype([0, 0, 0], ["Security", "Performance", "Speed"]))


    def test_init_model_with_prototype(self):
        expected_prototype = Prototype([0, 0, 0], [("DBMS", "Security"), ("DBMS", "Performance"), ("DBMS", "Speed")])
        actual_prototype = MoMoModel([self.multy_system.systems['DBMS']]).get_prototype()
        self.assertTrue(expected_prototype.equals(actual_prototype))


    def test_get_similarity_measures(self):
        self.model.get_similarity_measures()
        self.assertTrue(True)



if __name__ == '__main__':
	unittest.main()
