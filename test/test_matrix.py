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

from data.matrix import Table, TableException, TableOutOfBoundsException


class MyTestCase(unittest.TestCase):
    def test_table_init(self):
        t = Table()
        self.assertEqual(t, [])  # add assertion here
        self.assertEqual("Table[]", t.__repr__())
        self.assertRaises(TableOutOfBoundsException, Table, width=0)
        t = Table(width=3)
        self.assertEqual(t, [])  # add assertion here





if __name__ == '__main__':
    unittest.main()
