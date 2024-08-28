import set_pathes

import unittest
from momo.prototype import Prototype


class TestPrototype(unittest.TestCase):
    def test_init_prototype(self):
        prototype = Prototype(data=[1, 2, 3], index=['a', 'b', 'c'])
        self.assertEqual(prototype.to_list(), [1, 2, 3])


    def test_set_marks(self):
        prototype = Prototype(data=[1, 2, 3], index=['a', 'b', 'c'])
        prototype.set_marks([4, 5, 6])
        self.assertEqual(prototype.to_list(), [4, 5, 6])


    def test_set_incorect_marks(self):
        prototype = Prototype(data=[1, 2, 3], index=['a', 'b', 'c'])
        with self.assertRaises(ValueError):
            prototype.set_marks([4, 5, 6, 7])




if __name__ == '__main__':
	unittest.main()
