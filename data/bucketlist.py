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

from numbers import Number


class ContainerError(Exception):
    """
    Exception during bucket operations, typically when calling a method that can not operate on empty buckets
    """

    pass


class Container:
    """
    A container maintains statistical data about numerical data added to the container without storing the data itself
    Values can be added to container
    """

    def __init__(self) -> None:
        self._total = 0
        self._count = 0
        self._min = None
        self._max = None

    def __repr__(self) -> str:
        return f"Container(#{self._count},T={self._total},m={self._min},M={self._max}))"

    def __len__(self) -> int:
        return self.count()

    def __contains__(self, item):
        raise NotImplementedError()

    def __abs__(self):
        raise NotImplementedError()

    def __hex__(self):
        return hex(self._total)

    def __oct__(self):
        return oct(self._total)

    def __neg__(self):
        return -self._total

    def __pos__(self):
        return self._total

    def __int__(self):
        return int(self._total)

    def __eq__(self, other):
        """
        :type other: Container
        """
        return self._total == other._total and self._count == other._count and self._min == other._min and self._max == other.max

    def __lt__(self, other):
        """
        :type other: Container
        """
        if self._total != other._total:
            return self._total < other._total
        return self._count < other._count

    def __le__(self, other):
        """
        :type other: Container
        """
        return self.__eq__(other) or self._total < other._total or (self._total == other._total and self._total <= other._total)

    def __gt__(self, other):
        """
        :type other: Container
        """
        if self._total != other._total:
            return self._total > other._total
        return self._count > other._count

    def __ge__(self, other):
        """
        :type other: Container
        """
        return self.__eq__(other) or self._total > other._total or (self._total == other._total and self._total >= other._total)

    def __bool__(self):
        return self._total > 0

    def __ceil__(self):
        return self._total.__ceil__()

    def __floor__(self):
                return self._total.__floor__()

    def __and__(self, other):
        """
        :type other: Container
        """
        return self._count > 0 and other._count > 0

    def __or__(self, other):
        """
        :type other: Container
        """
        return self._count > 0 or other._count > 0

    def __xor__(self, other):
        """
        :type other: Container
        """

        return (self._count > 0) ^ (other._count > 0)

    def __sub__(self, other):
        raise NotImplementedError()

    def __add__(self,other):
        raise NotImplementedError()

    def append(self, value: Number) -> None:
        """
        Add a numeric value
        :param value: Value to add
        """
        self._count += 1
        self._total += value
        if self._min is None or value < self._min:
            self._min = value
        if self._max is None or value > self._max:
            self._max = value
        if self.store_values:
            super().append(value)

    def assert_count(self) -> None:
        """
        Helper function that raises an Exception when count is 0.
        This can be useful for functions that can not operate on empty buckets
        """
        if self._count == 0:
            raise BucketException("Cannot operate on an empty bucket")

    def store_values(self) -> book:
        """
        Get the store_values
        :return: _store_values
        """
        return self._store_values

    def total(self):
        """
        Get the total
        :return: _total
        """
        return self._total

    def count(self, *args, **kwargs):
        """
        Get the count
        :return: _count
        """
        return self._count

    def min(self):
        """
        Get the minimal value
        :return:  _min
        """
        self.assert_count()
        return self._min

    def max(self):
        """
        Get the maximal value
        :return:  _max
        """
        self.assert_count()
        return self._max

    def avg(self):
        """
        Get the average
        :return: average
        """
        self.assert_count()
        return self._total / self._count

    def __add__(self, other):
        if other is None:
            raise NotImplemented()
        if self._store_values != other.store_values:
            raise NotImplemented()
        if self._count == 0:
            self._min = other.min
            self._max = other.max
        elif other.count == 0:
            pass
        else:
            self._min = min(self._min, other.min)
            self._max = max(self._max, other.max)
        self._count += other.count
        self._total += other.total


class Bucket(list):
    """
    Base bucket functionality
    """

    def __init__(self, store_values=False) -> None:
        list.__init__(self)
        self._store_values = store_values
        self._total = 0
        self._count = 0
        self._min = None
        self._max = None

    def __repr__(self) -> str:
        list_str = f": {super()}" if self._store_values else ""
        return f"Bucket(#{self._count},T={self._total},min={self._min},max={self._max})  {list_str})"

    def __len__(self) -> int:
        if self._store_values:
            return list.__len__(self)
        else:
            return self.count()

    def __eq__(self, other):
        """
        :type other: Bucket
        """
        return self._total == other._total and self._count == other._count and self._min == other._min and self._max == other.max and self._store_values == other._store_values and (not  self._store_values or self.super() == other.super())

    def append(self, value: Number) -> None:
        """
        Add a numeric value
        :param value: Value to add
        """
        self._count += 1
        self._total += value
        if self._min is None or value < self._min:
            self._min = value
        if self._max is None or value > self._max:
            self._max = value
        if self.store_values:
            super().append(value)

    def assert_count(self) -> None:
        """
        Helper function that raises an Exception when count is 0.
        This can be useful for functions that can not operate on empty buckets
        """
        if self._count == 0:
            raise BucketException("Cannot operate on an empty bucket")

    def store_values(self) -> book:
        """
        Get the store_values
        :return: _store_values
        """
        return self._store_values

    def total(self):
        """
        Get the total
        :return: _total
        """
        return self._total

    def count(self, *args, **kwargs):
        """
        Get the count
        :return: _count
        """
        return self._count

    def min(self):
        """
        Get the minimal value
        :return:  _min
        """
        self.assert_count()
        return self._min

    def max(self):
        """
        Get the maximal value
        :return:  _max
        """
        self.assert_count()
        return self._max

    def avg(self):
        """
        Get the average
        :return: average
        """
        self.assert_count()
        return self._total / self._count

    def __add__(self, other):
        if other is None:
            raise NotImplemented()
        if self._store_values != other.store_values:
            raise NotImplemented()
        if self._count == 0:
            self._min = other._min
            self._max = other.max
        elif other.count == 0:
            pass
        else:
            self._min = min(self._min, other.min)
            self._max = max(self._max, other.max)
        self._count += other.count
        self._total += other.total


# class BucketList(dict):
#     """
#     A bucket list is an indexed list of buckets
#     """
#
#     def __init__(self, width, store_values) -> None:
#         """
#         :param width: Width of each bucket. The range  between min and max  must be a multiple of width
#         :param store_values: Indicate whether the individual values must be saved.
#         """
#         dict.__init__()
#         self._store_values
#         BaseBucket.__init__(self, store_values=store_values)
#         self.buckets = dict()
#         self.width = width
#
#     def __repr__(self) -> str:
#         ret = []
#         for key in self.sorted_keys():
#             ret.append(f"key: {key}, bucket= {self.buckets[key]}")
#         return f"<< BucketList {BaseBucket.__repr__(self)} Buckets: {ret} >>"
#
#     def sorted_keys(self):
#         """
#         Get the bucket indices in ascending order
#         :return: Sorted version
#         """
#         ret = list(self.buckets.keys())
#         ret.sort()
#         return ret
#
#     def disable_sampling(self) -> None:
#         """
#         Removes the values stored so far, the bucket will only keep track to count, total, min and max
#         """
#         self.store_values = False
#         for key, value in self.buckets.items():
#             value.disable_sampling()
#
#     def write_cvs_headers(self, file) -> None:
#         """
#         Write the CSV headers to file
#         :param file: file to write to
#         """
#         file.write(f"index;count;value")
#         if self.store_values:
#             file.write(";values")
#         file.write(os.linesep)
#
#     def write_csv_rows(self, file) -> None:
#         """
#         Write the CSV headers to file
#         :param file: file to write to
#         """
#         for key in self.sorted_keys():
#             file.write(f"{key}{SEPARATOR}{self.buckets.get(key)}")
#
#     def store_value(self, value: int) -> None:
#         """
#         Add a value to the list. The value is put in a bucket based on the range and bucket size.	 *
#         :param value: Value to add
#         """
#
#         key = math.floor(value / self.width)
#         target_bucket = self.buckets.get(key)
#         if target_bucket is None:
#             target_bucket = self.buckets[key] = Bucket(store_values=self.store_values)
#         target_bucket.add_value(value)
#
#     def percentiles(self, divider: int = 1) -> Matrix:
#         """
#         Calculate percentile of value buckets
#         :param divider: The bucket boundaries will be divided before returning.
#         :return:  Matrix [index, percentile]
#         """
#         # final Map<Long, Bucket> sorted = new TreeMap<>(buckets)
#         ret = Matrix(headers=["lower", "upper", "percentage"])
#         incremental = 0
#         for key in self.sorted_keys():
#             bucket = self.buckets[key]
#             incremental += bucket.count
#             row = [int(key * self.width / divider), int(key * self.width / divider) + 1, incremental / self.count]
#             ret.add_row(row)
#         return ret
#
#     def percentile(self, percentile: int) -> float:
#         """
#         Find the value for which the total count surpassed the request percentile.
#         :param percentile: Percentile to count up to
#         :return: the value corresponding
#         """
#         if not 0 < percentile <= 100:
#             raise BucketException("Percentile must be in [1,100]")
#         percentiles = self.percentiles()
#         for row in percentiles._data:
#             if row[1] >= percentile:
#                 return row.get[0]
#         raise BucketException("Percentile not reached")


if __name__ == "__main__":
    raise NotImplementedError(__file__)
