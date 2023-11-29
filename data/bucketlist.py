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

import os
from typing import Union


class BucketException(Exception):
    """
    Exceptions that occur during bucket operations, typically when calling a method that can not operate on empty buckets
    """
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class BaseBucket:
    """
    Base bucket functionality
    """

    def __init__(self, values: Union[list, set, tuple] = None, store_values=False) -> None:
        self.store_values = store_values
        self.total = 0
        self.count = 0
        self.min = None
        self.max = None
        if values is not None:
            for value in values:
                self.add_value(value)

    def __repr__(self) -> str:
        return f"count={self.count}, total={self.total}, min={self.min}, max={self.max}, keep_values={self.store_values}"

    def add_value(self, value: Union[int, float]) -> None:
        """
        Add a value
        :param value:
        """
        self.count += 1
        self.total += value
        if self.min is None or value < self.min:
            self.min = value
        if self.max is None or value > self.max:
            self.max = value
        self.store_value(value)

    def store_value(self, value):
        """
        store a value in the bucket
        :param value: value to store
        """
        pass
        raise NotImplementedError("store_value")

    def assert_count(self):
        """
        Helper function that raises an Exception when count is 0.
        This can be useful for functions that can not operate on empty buckets
        """
        if self.count == 0:
            raise BucketException("Cannot operate on an empty bucket")

    def minimum(self):
        """
        Get the minimum
        :return: values minimum
        """
        self.assert_count()
        return self.min

    def maximum(self):
        """
        Get the maximum
        :return: values maximum
        """
        self.assert_count()
        return self.max

    def average(self):
        """
        Get the average
        :return: values average
        """
        self.assert_count()
        return self.total / self.count


class Bucket(BaseBucket):
    """
    Representation of a bucket.
    When values are added to a bucket, several parameters are maintained:
        - total value
        - number of values
        - minimum
        - maximum
    If required, the individual can be kept in the bucket. This can be memory consuming
    """

    def __init__(self, values: Union[list, set, tuple] = None, store_values=False) -> None:
        """
        Create a bucket
        :param values: collection of values
        :param store_values: indicate if individual values must be stored
        """
        BaseBucket.__init__(self, values, store_values)
        self.values = []

    def __repr__(self) -> str:
        postfix = ""
        if self.store_values:
            postfix = f", values={self.values}"

        return f"<< Bucket={BaseBucket.__repr__(self)}{postfix} >>"

    def __len__(self) -> int:
        return self.count

    def store_value(self, value: int) -> None:
        """
        Add a value to the bucket and keep track of count, total, min, max. If {@code store_values} is set, then the value itself will be stored as well
        :param value: value to add
        """
        if self.store_values:
            self.values.append(value)

    def disable_sampling(self) -> None:
        """
        Removes the values stored so far, the bucket will only keep track to count, total, min and max
        """
        self.store_values = False
        self.values = None

    """
    public String csvData() {
        final StringBuilder sb = new StringBuilder(StringSize.MEDIUM)
        sb.append(count).append(FileTools.CSV_FIELD_SEPARATOR).append(total).append(FileTools.CSV_FIELD_SEPARATOR)
        if (store_values)
            for (final Long value : values)
                sb.append(value).append(FileTools.CSV_FIELD_SEPARATOR)
        return sb.toString()
    }

    public String csvHeaders() {
        return COUNT_HEADER + StringTools.FIELD_SEPARATOR + VALUE_HEADER + StringTools.FIELD_SEPARATOR
    }

    @SuppressWarnings("unchecked")
    @Override
    public JSONObject jsonData() {
        // todo: if present add individual values
        final JSONObject ret = new JSONObject()
        final JSONObject temp = new JSONObject()
        temp.put(VALUE_HEADER, total)
        temp.put(COUNT_HEADER, count)
        ret.put(BUCKET_HEADER, temp)
        return ret
    }

    @Override
    public Bucket parseJSON(final JSONObject jsonObject) {
        // todo: add parsing of individual values
        if (jsonObject == null)
            throw new NullPointerException(StringTools.text(Text.ERROR_NULL_NOT_ALLOWED))
        if (jsonObject.keySet().size() != 1 || !jsonObject.containsKey(BUCKET_HEADER))
            throw new InvalidParameterException(StringTools.text(Text.JSON_HIGHEST_LEVEL_ERROR, BUCKET_HEADER))
        final Object object = jsonObject.get(BUCKET_HEADER)
        if (!(object instanceof JSONObject sub_object))
            throw new InvalidParameterException("Highest level must 1 item named '" + BUCKET_HEADER + "'")
        if (sub_object.keySet().size() != 2 || !sub_object.containsKey(VALUE_HEADER) || !sub_object.containsKey(COUNT_HEADER))
            throw new InvalidParameterException("sub level must contain 2 item named '" + COUNT_HEADER + "' and '" + VALUE_HEADER + "'")
        final Bucket ret = new Bucket()
        ret.total = (Long) sub_object.get(VALUE_HEADER)
        ret.count = (Integer) sub_object.get(COUNT_HEADER)
        return ret
    }

     * Create a bucket that contains the data of two other buckets.
     *
     * @param left  first bucket to merge
     * @param right second bucket to merge
     * @return new bucket with data of both buckets, correct minimum, maximum and if enabled: individual values of both buckets
     * @throws NullPointerException     if either bucket is null
     * @throws IllegalArgumentException if one bucket stores individual value and the other doesn't
    public static Bucket merge(final Bucket left, final Bucket right) {
        if (left == null || right == null)
            throw new NullPointerException("Can not merge null-buckets.")
        if (left.store_values != right.store_values)
            throw new IllegalArgumentException("Can not merge buckets with different value for store-values")
        final Bucket ret = new Bucket()
        ret.count = left.count + right.count
        ret.total = left.total + right.total
        ret.maximum = Math.max(left.maximum, right.maximum)
        ret.minimum = Math.min(left.minimum, right.minimum)
        ret.store_values = left.store_values
        if (ret.store_values) {
            ret.values.addAll(left.values)
            ret.values.addAll(right.values)
        }
        return ret
    }

    """


class BucketList(BaseBucket):
    """
    A bucket list is an indexed list of buckets
    """

    def __init__(self, width, store_values) -> None:
        """
        :param width:          Width of each bucket. The range  between min and max  must be a multiple of width
        :param store_values: Indicate whether the individual values must be saved.
        """
        BaseBucket.__init__(self, store_values=store_values)
        self.buckets = dict()
        self.width = width

    def __repr__(self) -> str:
        ret = []
        for key in self.sorted_keys():
            ret.append(f"key: {key}, bucket= {self.buckets[key]}")
        return f"<< BucketList {BaseBucket.__repr__(self)} Buckets: {ret} >>"

    def sorted_keys(self):
        """
        Get the bucket indices in ascending order
        :return: Sorted version
        """
        ret = list(self.buckets.keys())
        ret.sort()
        return ret

    def disable_sampling(self) -> None:
        """
        Removes the values stored so far, the bucket will only keep track to count, total, min and max
        """
        self.store_values = False
        for key, value in self.buckets.items():
            value.disable_sampling()

    def write_cvs_headers(self, file) -> None:
        """
        Write the CSV headers to file
        :param file: file to write to
        """
        file.write(f"index;count;value")
        if self.store_values:
            file.write(";values")
        file.write(os.linesep)

    def write_csv_rows(self, file) -> None:
        """
        Write the CSV headers to file
        :param file: file to write to
        """
        for key in self.sorted_keys():
            file.write(f"{key}{SEPARATOR}{self.buckets.get(key)}")

    def store_value(self, value: int) -> None:
        """
        Add a value to the list. The value is put in a bucket based on the range and bucket size.	 *
        :param value: Value to add
        """

        key = math.floor(value / self.width)
        target_bucket = self.buckets.get(key)
        if target_bucket is None:
            target_bucket = self.buckets[key] = Bucket(store_values=self.store_values)
        target_bucket.add_value(value)

    def percentiles(self, divider: int = 1) -> Matrix:
        """
        Calculate percentile of value buckets
        :param divider: The bucket boundaries will be divided before returning.
        :return:  Matrix [index, percentile]
        """
        # final Map<Long, Bucket> sorted = new TreeMap<>(buckets)
        ret = Matrix(headers=["lower", "upper", "percentage"])
        incremental = 0
        for key in self.sorted_keys():
            bucket = self.buckets[key]
            incremental += bucket.count
            row = [int(key * self.width / divider), int(key * self.width / divider) + 1, incremental / self.count]
            ret.add_row(row)
        return ret

    def percentile(self, percentile: int) -> float:
        """
        Find the value for which the total count surpassed the request percentile.
        :param percentile: Percentile to count up to
        :return: the value corresponding
        """
        if not 0 < percentile <= 100:
            raise BucketException("Percentile must be in [1,100]")
        percentiles = self.percentiles()
        for row in percentiles._data:
            if row[1] >= percentile:
                return row.get[0]
        raise BucketException("Percentile not reached")


if __name__ == "__main__":
    raise NotImplementedError(__file__)
