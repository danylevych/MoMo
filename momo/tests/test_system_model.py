import set_pathes

import pandas as pd
import unittest
from momo.system_models.system_models import SystemModel



class TestSystemModel(unittest.TestCase):
    def setUp(self):
        self.system_model = SystemModel("test_model", [[1, 2, 3], [4, 5, 6], [7, 8, 9]], features=['f1', 'f2', 'f3'], alternatives=["a1", "a2", "a3"])


    def test_init_system_model_incorect_name(self):
        with self.assertRaises(ValueError):
            SystemModel(name=None)


    def test_init_system_model_incorect_features(self):
        with self.assertRaises(ValueError):
            SystemModel(name="test", data=[[1, 2, 3], [4, 5, 6], [7, 8, 9]], features=['f1', 'f2'], alternatives=["a1", "a2", "a3"])


    def test_init_system_model_with_data_only(self):
        system_model = SystemModel(name="test", data=[[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        self.assertEqual(system_model.data.index.to_list(), [0, 1, 2])
        self.assertEqual(system_model.data.columns.to_list(), [0, 1, 2])

    def test_init_system_model_with_data_frame(self):
        system_model = SystemModel(name="test", data=pd.DataFrame([[1, 2, 3], [4, 5, 6], [7, 8, 9]], columns=['f1', 'f2', 'f3'], index=['a1', 'a2', 'a3']))
        self.assertEqual(system_model.data.index.to_list(), ['a1', 'a2', 'a3'])
        self.assertEqual(system_model.data.columns.to_list(), ['f1', 'f2', 'f3'])

    def test_init_system_model_incorect_alternatives(self):
        with self.assertRaises(ValueError):
            SystemModel(name="test", data=[[1, 2, 3], [4, 5, 6], [7, 8, 9]], features=['f1', 'f2', 'f3'], alternatives=["a1", "a2"])


    def test_init_system_model(self):
        system_model = SystemModel("test")
        self.assertEqual(system_model.name, "test")


    def test_init_system_model(self):
        self.assertEqual(self.system_model.data['a1'].to_list(), [1, 4, 7])


    def test_add_feature(self):
        self.system_model.add_feature('f4', [10, 11, 12])
        self.assertEqual(self.system_model.loc['f4'].to_list(), [10, 11, 12])


    def test_add_feature_incorect_length(self):
        with self.assertRaises(ValueError):
            self.system_model.add_feature('f4', [10, 11])


    def test_add_feature_incorect_name(self):
        with self.assertRaises(ValueError):
            self.system_model.add_feature(None, [10, 11, 12])


    def test_add_alternative(self):
        self.system_model.add_alternative('a4', [13, 14, 15])
        self.assertEqual(self.system_model['a4'].to_list(), [13, 14, 15])


    def test_add_alternative_incorect_length(self):
        with self.assertRaises(ValueError):
            self.system_model.add_alternative('a4', [13, 14])


    def test_add_alternative_incorect_name(self):
        with self.assertRaises(ValueError):
            self.system_model.add_alternative(None, [13, 14, 15])


    def test_remove_alternative(self):
        self.system_model.remove_alternative('a1')
        self.assertNotIn('a1', self.system_model.data.columns)


    def test_remove_alternative_incorect_key(self):
        self.system_model.remove_alternative('a1')
        with self.assertRaises(KeyError):
            self.system_model['a1']


    def test_remove_feature(self):
        self.system_model.remove_feature('f1')
        self.assertNotIn('f1', self.system_model.data.index)


    def test_remove_features_incorect_key(self):
        self.system_model.remove_feature('f1')
        with self.assertRaises(KeyError):
            self.system_model.loc['f1']



if __name__ == "__main__":
    unittest.main()
