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
from data.bucketlist import Bucket, BucketException

class MyTestCase(unittest.TestCase):
    def test_bucket(self):
        b = Bucket()
        self.assertEqual(False, b.store_values)
        self.assertEqual(0, b.count())
        self.assertEqual(0, b.total)
        self.assertRaises(BucketException, b.avg)
        self.assertRaises(BucketException, b.max)
        self.assertRaises(BucketException, b.min)


if __name__ == '__main__':
    unittest.main()
