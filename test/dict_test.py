""" 
This file is part of tolyn.    

tolyn is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
       
"""

import unittest
from data.dict import Dict, DictException

KEYS = ['A', 'B', 'C', 'D']
VALUES = [4, 3, 2, 1]
TEST_DATA = [(KEYS[i], VALUES[i]) for i in range(len(KEYS))]


class MyTestCase(unittest.TestCase):
    def test_remove_keys(self):
        d = Dict()
        d.update(TEST_DATA)
        self.assertEqual(KEYS, list(d.keys()))
        self.assertEqual(VALUES, list(d.values()))
        self.assertIsNone(d.remove_keys('B', 'C'))
        self.assertRaises(KeyError, d.remove_keys, 'A', raise_if_not_empty=True)
        self.assertEqual(['D'], list(d.keys()))

    def test_valueslist(self):
        d = Dict()
        d.update(TEST_DATA)
        self.assertEqual(KEYS, d.keyslist())
        self.assertEqual(VALUES, d.valueslist())


if __name__ == '__main__':
    unittest.main()
