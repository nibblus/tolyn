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

import copy
import os
from typing import Optional


HTML_TABLE_LIMIT_DEFAULT = 50
ALLOWED_ROW_TYPES = [list, tuple]


class MatrixException(Exception):
    """
    Matrix specific exceptions
    """

    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class MatrixOutOfBoundsException(MatrixException):
    """
    Matrix specific exceptions
    """

    def __init__(self, msg: str) -> None:
        super().__init__(f"MatrixOutOfBoundsException: {msg}")


class Matrix:
    """
    Matrix representation
    """

    def __init__(self, **kwargs) -> None:
        """
        Creates a two dimensional matrix
        :param kwargs:
            width, height (default 0), default_value (default None)
        """
        self._headers = []
        self._data = []
        if kwargs.get("string_value") is not None:
            self.from_json(kwargs.get("string_value"))
            return

        width = kwargs.get('width')
        if width is not None:
            if width < 1:
                raise MatrixOutOfBoundsException("width must be at least 1")
            for x in range(width):
                self._headers.append(str(x))
            height = kwargs.get('height', 0)
            default_value = kwargs.get('default_value', None)
            for y in range(height):
                row = []
                for x in range(width):
                    row.append(default_value)
                self._data.append(row)
        headers = kwargs.get("headers")
        if headers is not None:
            self.set_headers(headers)

    # noinspection PyProtectedMember
    def __eq__(self, other):
        return self._headers == other._headers and self._data == other._data

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return self._data.__iter__()

    def __getitem__(self, i):
        return self._data[i]

    # representation methods
    def __repr__(self):
        ret = f"Matrix[{os.linesep}Headers: {self._headers}{os.linesep}"
        if self.contains_data():
            for row in self._data:
                ret += str(row) + os.linesep
        else:
            ret += f"No data {os.linesep}"
        return f"{ret}]"

    def json(self) -> str:
        """
        JSON representation
        :return: JSON string
        """

        headers = []
        for i in range(len(self._headers)):
            d = dict()
            d[INDEX] = i
            d[NAME] = self._headers[i]
            d[CLASS] = "str"
            if len(self._data) > 0:
                d[CLASS] = type(self._data[0][i]).__name__
            headers.append(d)
        matrix = []
        for row in self._data:
            d = dict()
            for i in range(len(row)):
                d[str(i)] = str(row[i])
            matrix.append(d)
        json_str = f'{{"{HEADERS}":{headers},"{MATRIX}":{matrix}}}'.replace("'", '"')
        return json_str

    def from_json(self, string: str):
        """
        Convert string to matrix
        :param string: json string
        :return: matrix
        """
        raise NotImplementedError

    # def html(self, show_index: bool = False, limit: int = HTML_TABLE_LIMIT_DEFAULT) -> str:
    #     """
    #     Convert a Matrix into an HTML table
    #     :param show_index: if true a first column will be added to show the row index
    #     :param limit: max number of lines to be printed
    #     :return: html code
    #     """
    #
    #     html_code = f"{html.TABLE_OPEN}{html.ROW_OPEN}"
    #     if show_index:
    #         html_code += f"{html.TABLE_HEADER_OPEN}#{html.TABLE_HEADER_CLOSE}"
    #     for title in self._headers:
    #         html_code += f"{html.TABLE_HEADER_OPEN}{title}{html.TABLE_HEADER_CLOSE}"
    #     html_code += html.ROW_CLOSE
    #     if self.is_empty():
    #         html_code += html.ROW_OPEN
    #         for i in range(len(self._headers)):
    #             html_code += html.EMPTY_CELL
    #         html_code += html.ROW_CLOSE
    #     else:
    #         for i in range(len(self._data)):
    #             html_code += html.ROW_OPEN
    #             if show_index:
    #                 html_code += f"{html.TABLE_HEADER_OPEN}{i + 1}{html.TABLE_HEADER_CLOSE}"
    #             html_code += html.list_to_table_row(self._data[i], False)
    #             html_code += html.ROW_CLOSE
    #             if i >= limit:
    #                 j = 0
    #                 if show_index:
    #                     j = 1
    #                 html_code += f"{html.ROW_OPEN}<TD colspan='{len(self._headers) + j}'>More rows are available but only the first {limit} rows are shown.{html.TABLE_CELL_CLOSE}{html.ROW_CLOSE}"
    #                 break  # To exit if limit lines reached
    #     html_code += html.TABLE_CLOSE
    #     return html_code

    # Consistency checkers
    @staticmethod
    def check_row_type(value, raise_exception: bool = False) -> bool:
        """
        Verify if type is ok. Typically, row must be a list or a tuple
        :param value: Value to check
        :param raise_exception: raise an exception if the matrix is not initialized
        :return: True if type is ok
        """
        if type(value) not in ALLOWED_ROW_TYPES:
            if raise_exception:
                raise MatrixException("row is of wrong type")
            return False
        return True

    @staticmethod
    def check_row(row, raise_exception: bool = False) -> bool:
        """
        Determine if type and length of a value or ok. Typically, row must be a list or a tuple. Length must be equal to the number of headers
        :param row: value to check
        :param raise_exception: raise an exception if the matrix is not initialized
        :return: true is Matrix is not yet initialized
        """
        if not Matrix.check_row_type(row, raise_exception) or len(row) == 0:
            return False

    def check_headers(self, raise_exception: bool = False) -> bool:
        """
        Check if headers are set correctly
        :param raise_exception: raise an exception if the matrix is not initialized
        :return: True of False
        """
        if self._headers is None or self._headers == []:
            if raise_exception:
                raise MatrixOutOfBoundsException(f"headers are none or empty.")
            return False
        if type(self._headers) not in ALLOWED_ROW_TYPES:
            if raise_exception:
                raise MatrixException(f"{type(self._headers)} is in {ALLOWED_ROW_TYPES}")
            return False
        return True

    def within_row_range(self, *args, raise_exception: bool = False) -> bool:
        """
        Check if values are within the row range
        :param raise_exception:
        :param args:
        :return:
        """
        for arg in args:
            if not (0 <= arg < len(self._data)):
                if raise_exception:
                    raise MatrixOutOfBoundsException(f"row index {arg} out of bounds")
                return False
        return True

    def within_column_range(self, *args, raise_exception: bool = False) -> bool:
        """
        Check if args are in range of the matrix width
        :param args: value
        :param raise_exception: if True an exception will be raised in case of error
        :return:
        """
        for arg in args:
            if self._headers == [] or not (0 <= arg < len(self._headers)):
                if raise_exception:
                    raise MatrixOutOfBoundsException(f"col index {arg} out of bounds")
                return False
        return True

    def is_empty(self) -> bool:
        """
        Check is matrix contains data
        :return: True if matrix contains no rows, False otherwise
        """
        self.check_headers()
        return len(self._data) == 0

    def contains_data(self) -> bool:
        """
        Check is matrix contains data
        :return: True if matrix contains rows, False otherwise
        :return:
        """
        return not self.is_empty()

    def dimensions(self) -> Vector:
        """
        Get the dimensions of the matrix
        :return: (heigth, width)
        """
        return Vector(len(self._data), len(self._headers))

    # todo: unittest
    def add(self, other_matrix) -> None:
        """
        Add the data of another matrix
        :param other_matrix: matrix to add
        """
        self._data += other_matrix._data

    def width(self) -> int:
        """
        Get width of the matrix
        :return: width
        """
        length = len(self._headers)
        if length > 0:
            return length
        raise MatrixException("Not initialized")

    # data getters and setters
    def set_headers(self, headers: list) -> None:
        """
        Set the headers of the matrix.
        Note: Existing headers can only be updated if the new list has the same size or the matrix is still empty
        :param headers: list of header
        """
        if len(self._data) == 0 or len(self._headers) == 0 or len(self._headers) == len(headers):
            self._headers = strings.list_stringify(headers)
        else:
            raise MatrixException("Can not set headers: matrix is not empty or new size does not equal old size")

    def add_row(self, row: list) -> None:
        """
        Add a row to the matrix
        :param row: Row to add
        """
        self.check_row(row, True)  # will throw exception in case of problems
        if len(self._headers) != len(row):
            if len(self._headers) == 0:
                self.set_headers([x for x in range(len(row))])
            raise MatrixOutOfBoundsException(f"row width ({len(row)} does not match header width {len(self._headers)}")
        if type(row) == list:
            self._data.append(row)
        else:
            self._data.append(list(row))

    def get_row(self, row_index: int):
        """
        Get a row from the matrix
        :param row_index: index row
        :return: specific row
        """
        self.within_row_range(row_index, True)
        return self._data[row_index]

    # unit test ok
    def column(self, index: int = 0) -> list:
        """
        Get a column from the matrix
        :param index: 0-index of the column.
        :return: list containing the data of the selected column.
        """
        self.within_column_range(index, raise_exception=True)
        column_list = []
        for row in self._data:
            column_list.append(row[index])
        return column_list

    # calculators
    def column_function(self, functions):
        """
        Apply a function to each column, e.g. max, min
        :return:  list of maxima, one for each column
        """
        ret = []
        for i in range(len(self._headers)):
            ret.append(functions(i))
        return ret

    # unit test ok
    def column_max(self, column: int):
        """
        Get the maximum value in a column
        : param column:  Index of the column
        : return : Maximum value of the column
        """
        temp_max = self._data[0][column]
        for i in range(len(self._data) - 1):
            value = self._data[i + 1][column]
            if value > temp_max:
                temp_max = value
        return temp_max

    # unit test ok
    def column_min(self, column: int):
        """
        Get the min value in a column
        :param column:  Index of the column
        :return : Minimum value of the column
        """
        temp_min = self._data[0][column]
        for i in range(len(self._data) - 1):
            value = self._data[i + 1][column]
            if value < temp_min:
                temp_min = value
        return temp_min

    # unit test ok
    def minima(self):
        """
        Get the min value of all columns
        :return : Minimum value of  all  columns
        """
        return self.column_function(self.column_min)

    # unit test ok
    def maxima(self):
        """
        Get the max value of all columns
        :return : Max value of  all  columns
        """
        return self.column_function(self.column_max)

    # manipulators
    # unit test ok
    def swap_columns(self, first: int, second: int) -> None:
        """
        swap two columns
        :param first: index of the first column
        :param second: index of the second column
        """
        self.within_column_range(first, second)
        temp = self._headers[first]
        self._headers[first] = self._headers[second]
        self._headers[second] = temp
        for i in range(len(self._data)):
            temp = self._data[i][first]
            self._data[i][first] = self._data[i][second]
            self._data[i][second] = temp

    # unittest ok
    def reverse(self) -> None:
        """
        reverse the order of rows in the matrix
        """
        if len(self._data) < 2:
            return
        for i in range(int(len(self._data) / 2) + 1):
            index = len(self._data) - i - 1
            temp = self._data[i]
            self._data[i] = self._data[index]
            self._data[index] = temp

    def delete_column(self, column: int) -> None:
        """
        delete a column from the matrix
        :param column: column 0-based index of the column
        """
        self.within_column_range(column)
        self._headers.pop(column)
        for row in self._data:
            row.pop(column)

    def add_column(self, column: Optional[int], header: str = "", initial=None) -> None:
        """
        Add a column to the matrix
        :param column: column 0-based index of the column
        :param header: 
        """
        # todo : add error handling and argument documentation
        self.within_column_range(column)
        self._headers.insert(column, header)
        for row in self._data:
            row.insert(column, initial)

    # miscellaneous
    def to_csv_file(self, full_file_path: str, separator: chr = ';') -> None:
        """
        write matrix to CSV file
        :param full_file_path: full path name
        :param separator: separator
        """
        file = open(full_file_path, "wt")
        for header in self._headers:
            file.write(f"{header}{separator}")
        file.write(os.linesep)
        for row in self._data:
            for value in row:
                file.write(f"{value}{separator}")
            file.write(os.linesep)
        file.close()

    # unit test ok
    def create_with_same_headers(self):
        """
        Create a new empty matrix with the same headers as the provided matrix

        :return: Empty matrix (no rows) with same headers as the original
        """
        return Matrix(headers=copy.deepcopy(self._headers))

    def eliminate_doubles(self) -> None:
        """
        Eliminate subsequent identical rows from the matrix.
        """
        if len(self._data) < 2:
            return
        previous_row = self._data[0]
        temp_data = [previous_row]
        i = 1
        while i < len(self._data):
            current_row = self._data[i]
            i += 1
            if current_row == previous_row:
                continue
            temp_data.append(current_row)
            previous_row = current_row
        self._data = temp_data

    def sort(self, sort_function=None):
        """
        Sort the matrix
        :param sort_function:
        :return:
        """
        if len(self._data) < 2:
            return  # nothing to sort
        self._data.sort(key=sort_function)

    def get(self, x, y=None) -> object:
        """
        Get a cell or a row from the matrix
        :param x: row to get
        :param y: element for find with the row. If None the whole row is returned
        :return: element or row
        """
        if y is None:
            return self._data[x]
        return self._data[x][y]

    def set(self, x: int, y: int, value) -> None:
        """
        Set a specific value in the matrix
        :param x: row index
        :param y: column index
        :param value: new value
        """
        self._data[x][y] = value

    def height(self) -> int:
        """
        Get height of the matrix
        :return:
        """
        return len(self._data)

    def minus(self, right):
        """
        Subtract two matrices
        :param right: matrix to subtract
        :return: Result of subtrction
        """
        return subtract(self, right)


def subtract(remove_from: Matrix, to_remove: Matrix) -> Matrix:
    """

    :param remove_from:
    :param to_remove:
    :return:
    """
    if remove_from._headers == [] or to_remove._headers == []:
        raise MatrixException("parameters must not be empty")
    if remove_from.width() != to_remove.width():
        raise MatrixException("parameters must be same width")
    left = copy.deepcopy(remove_from)
    if left.is_empty():
        return left
    left.sort()
    right = copy.deepcopy(to_remove)
    if right.is_empty():
        return left
    right.sort()
    ret = Matrix(headers=left._headers)
    left_row = left.get(0)
    right_row = right.get(0)
    i = j = 0

    while i < left.height() and j < right.height():
        if left_row > right_row:
            while j < right.height() and left_row > right_row:
                j += 1
                if j < right.height():
                    right_row = right.get(j)
        elif left_row == right_row:
            while i < left.height() and left.get(i) == left_row:
                i += 1
            if i < left.height():
                left_row = left.get(i)
            while j < right.height() and right.get(j) == right_row:
                j += 1
            if j < right.height():
                right_row = right.get(j)
        else:
            while i < left.height() and left_row < right_row:
                ret.add_row(left_row)
                i += 1
                if i < left.height():
                    left_row = left.get(i)
    while i < left.height():
        ret.add_row(left.get(i))
        i += 1
    return ret


def comm(orig_left: Matrix, orig_right: Matrix) -> (Matrix, Matrix, Matrix):
    """
    Takes to two Matrices columns and create a map of three Matrices
    Similar to the linux command comm
    :param orig_left: left matrix
    :param orig_right: right matrix
    :return: dict()
        dict 'LEFT' : rows only present in the original left matrix
        dict 'RIGHT' : rows only present in the original right matrix
        dict 'BOTH' : rows  present both  matrices
    """
    left = copy.deepcopy(orig_left)
    right = copy.deepcopy(orig_right)
    left.sort()
    right.sort()
    left.eliminate_doubles()
    right.eliminate_doubles()
    comm_left = Matrix(headers=left._headers)
    comm_right = Matrix(headers=left._headers)
    comm_both = Matrix(headers=left._headers)
    left_index = right_index = 0
    while left_index < left.height() and right_index < right.height():
        row_left = left.get(left_index)
        row_right = right.get(right_index)
        if row_left < row_right:
            comm_left.add_row(left.get(left_index))
            left_index += 1
        elif row_left == row_right:
            comm_both.add_row(left.get(left_index))
            left_index += 1
            right_index += 1
        else:
            comm_right.add_row(right.get(right_index))
            right_index += 1

    while left_index < left.height():
        comm_left.add_row(left.get(left_index))
        left_index += 1

    while right_index < right.height():
        comm_right.add_row(right.get(right_index))
        right_index += 1

    return comm_left, comm_both, comm_right


HEADERS = "HEADERS"
MATRIX = "MATRIX"
NAME = "NAME"
CLASS = "CLASS"
INDEX = "INDEX"

import json
from json import JSONDecodeError


def create_from_json(json_string: str) -> Optional[Matrix]:
    """
    Create a matrix from JSON
    :param json_string:  json data
    :return : matrix version of the json data
    """

    ret = Matrix()
    try:
        json_value = json.loads(json_string)
        header_name, header_class = json_headers_to_matrix_headers(json_value.get(HEADERS))
        ret.set_headers(header_name)
        json_matrix_to_matrix_data(json_value.get(MATRIX), header_class, ret)
    except JSONDecodeError as e:
        SCRIPT_LOGGER.warning(f"Cannot parse value {json_string} : {e}")
        return None
    return ret

    # raise NotImplementedError("create_from_json() meot nog uitgebreid worden zodat tpyes geconverteerd worden van str naar het eigenlijke type")  # to: implement from_json


def json_headers_to_matrix_headers(json_value: dict) -> (list, list):
    """
    Helper function to convert json header data into Matrix headers
    :param json_value:   json array
    """
    names = []
    classes = []
    for i in range(len(json_value)):
        names.append("")
        classes.append("")

    for value in json_value:
        index = int(value.get(INDEX))
        names[index] = value.get(NAME)
        classes[index] = value.get(CLASS)

    return names, classes


def json_matrix_to_matrix_data(json_value: dict, classes: list, matrix: Matrix) -> None:
    """
    Helper function to convert json matrix data into Matrix type
    :param json_value:    json array
    :param classes:  List of classes, one per column.
    :param matrix: Matrix to store the internals in.
    """
    for value in json_value:
        row = []
        r = range(len(classes))
        for i in r:
            row.append(None)
        for i in r:
            row[i] = value[str(i)]
            if classes[i] == "int":
                row[i] = int(row[i])
        matrix.add_row(row)


def differences(left: Matrix, right: Matrix) -> Matrix:
    """
    :param left:
    :param right:
    :return:
    """
    l, b, r = comm(left, right)
    ret = Matrix(headers=left._headers)
    ret._data = l._data + r._data
    return ret


if __name__ == '__main__':
    raise NotImplementedError(__file__)
