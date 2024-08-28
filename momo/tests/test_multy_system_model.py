import pandas as pd
import set_pathes

import unittest
from momo.system_models.system_models import SystemModel, MultiSystemModel



class TestMultySystemModel(unittest.TestCase):
    def setUp(self):
        self.dbms = SystemModel("DBMS")
        self.dbms.add_feature("Security", {"MySQL": 1, "MS SQL": 1, "Oracle": 1})
        self.dbms.add_feature("Performance", [1, 1, 1])
        self.dbms.add_feature("Speed", [0, 1, 1])

        self.connector = SystemModel("Connector")
        self.connector.add_feature("Flexibility", {"Copper": 1, "Aluminum": 1})
        self.connector.add_feature("Cost", {"Copper": 1, "Aluminum": 1})


    def test_init_multi_system_model(self):
        multi_system_model = MultiSystemModel([self.dbms])
        self.assertEqual(multi_system_model.systems, {"DBMS": self.dbms})


    def test_init_multi_system_model_with_tuple(self):
        multi_system_model = MultiSystemModel((self.dbms, self.connector))
        self.assertEqual(multi_system_model.systems, {"DBMS": self.dbms, "Connector": self.connector})


    def test_init_multi_system_model_with_set(self):
        multi_system_model = MultiSystemModel({self.dbms, self.connector})
        self.assertEqual(multi_system_model.systems, {"DBMS": self.dbms, "Connector": self.connector})


    def test_init_multi_system_model_incopatible_type(self):
        with self.assertRaises(ValueError):
            MultiSystemModel("DBMS")


    def test_init_multi_system_model_none(self):
        multi_system_model = MultiSystemModel()
        self.assertEqual(multi_system_model.systems, {})


    def test_add_system(self):
        multi_system_model = MultiSystemModel()
        multi_system_model.add_system(self.dbms)
        self.assertEqual(multi_system_model.systems, {"DBMS": self.dbms})


    def test_add_system_incopatible_type(self):
        multi_system_model = MultiSystemModel()
        with self.assertRaises(ValueError):
            multi_system_model.add_system("DBMS")


    def test_add_systems(self):
        multi_system_model = MultiSystemModel()
        multi_system_model.add_systems([self.dbms, self.connector])
        self.assertEqual(multi_system_model.systems, {"DBMS": self.dbms, "Connector": self.connector})


    def test_add_systems_incopatible_type(self):
        multi_system_model = MultiSystemModel()
        with self.assertRaises(ValueError):
            multi_system_model.add_systems("DBMS")


    def test_remove_system(self):
        multi_system_model = MultiSystemModel([self.dbms, self.connector])
        multi_system_model.remove_system("DBMS")
        self.assertEqual(multi_system_model.systems, {"Connector": self.connector})


    def test_remove_system_not_found(self):
        multi_system_model = MultiSystemModel([self.dbms, self.connector])
        with self.assertRaises(ValueError):
            multi_system_model.remove_system("DBMS1")


    def test_get_prototype(self):
        multi_system_model = MultiSystemModel([self.dbms, self.connector])
        prototype = multi_system_model.get_prototype()
        expected_prototype = pd.Series({
            ("DBMS", "Security"): 0,
            ("DBMS", "Performance"): 0,
            ("DBMS", "Speed"): 0,
            ("Connector", "Flexibility"): 0,
            ("Connector", "Cost"): 0,
        })

        self.assertTrue(prototype.equals(expected_prototype))


    def test_get_prototype_with_one_system(self):
        multi_system_model = MultiSystemModel([self.dbms])
        prototype = multi_system_model.get_prototype()
        expected_prototype = pd.Series({
            ("DBMS", "Security"): 0,
            ("DBMS", "Performance"): 0,
            ("DBMS", "Speed"): 0,
        })

        self.assertTrue(prototype.equals(expected_prototype))


    def test_get_prototype_with_empty_systems(self):
        multi_system_model = MultiSystemModel()
        prototype = multi_system_model.get_prototype()
        expected_prototype = pd.Series({})

        self.assertTrue(prototype.equals(expected_prototype))


    def test_get_all_combinations(self):
        multi_system_model = MultiSystemModel([self.dbms, self.connector])
        combinations = multi_system_model.get_all_combinations()
        expected_combinations = pd.DataFrame(data={
            ("DBMS", "Security"):         [1, 1, 1, 1, 1, 1],
            ("DBMS", "Performance"):      [1, 1, 1, 1, 1, 1],
            ("DBMS", "Speed"):            [0, 0, 1, 1, 1, 1],
            ("Connector", "Flexibility"): [1, 1, 1, 1, 1, 1],
            ("Connector", "Cost"):        [1, 1, 1, 1, 1, 1],
        }, index=[('MySQL', 'Copper'), ('MySQL', 'Aluminum'),
                ('MS SQL', 'Copper'), ('MS SQL', 'Aluminum'),
                ('Oracle', 'Copper'), ('Oracle', 'Aluminum'),])

        self.assertTrue(combinations.equals(expected_combinations.transpose()))



if __name__ == "__main__":
    unittest.main()
