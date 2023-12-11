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
from ctypes import Union


def starts_with_from_list(string: str, prefixes: list, case_sensitive: bool = True) -> bool:
    """
    Check if a string starts with any
    :param string: value to check
    :param prefixes: list of strings
    :param case_sensitive: case modus
    :return: true if the string starts with any of the prefixes in the list
    """
    if string is None:
        raise Warning(error_invalid_param_type('string', string))
    if none_or_empty(prefixes):
        raise Warning(error_invalid_param_type('string', string))
    for prefix in prefixes:
        if case_sensitive:
            if string.startswith(prefix):
                return True
        else:
            if string.upper().startswith(prefix.upper()):
                return True
    return False


def get_epoch_now() -> int:
    """
    Get the current epoch time
    :return: Epoch time
    """
    return int(time.time())


def count_nones(*args) -> int:
    """
    Count the number of None arguments
    :param args: list of arguments
    :return: Number of Nones
    """
    count = 0
    for value in args:
        if value is None:
            count += 1
    return count


def count_not_nones(*args) -> int:
    """
    Count the number of not None arguments
    :param args: list of arguments
    :return: Number of non None values
    """
    count = 0
    for value in args:
        if value is not None:
            count += 1
    return count


def get_first_non_none(*args) -> object:
    """
    Get the first non None value from the arguments
    :param args: list of arguments
    :return: First non None value
    """
    for value in args:
        if value is not None:
            return value
    raise exceptions.FrameworkException("No not none value found in list {*args}")


def none_or_empty(value) -> bool:
    """
    Determine whether a value is None or empty
    :param value: Value to check
    :return: True is value is None or empty
    """
    if value is None:
        return True
    if type(value) in [str, list, dict, set, tuple]:
        return len(value) == 0
    return False


def not_none_or_empty(value) -> bool:
    """
    Determine whether a value is None or empty
    :param value: Value to check
    :return: True is value is None or empty
    """
    return not none_or_empty(value)


def split_list(input_list: list, size: int, complete_last: bool = False, default_value=None) -> list:
    """
    Split a list in parts of a specific size.
    :param input_list: list to split
    :param size: size of the sub lists
    :param complete_last: If true, default values will be added to the last part in order to match the size
    :param default_value: Use this value in case complete_last is true, otherwise ignore this parameter
    """
    if size < 1:
        raise exceptions.FrameworkException(f"Size {size} must be strictly positive")
    ret = []
    if none_or_empty(list):
        return ret
    for i in range(math.ceil(len(input_list) / size)):
        start = i * size
        end = (i + 1) * size
        ret.append(input_list[start:end])
    if complete_last:
        length = len(ret[-1])
        if length < size:
            for i in range(size - length):
                ret[-1].append(default_value)
    return ret


def add_to(target: Union[list, set], value) -> None:
    """
    Add a value to a list or a set
    :param value: Value to add
    :param target: set or list to add value to
    """
    if isinstance(target, list):
        target.append(value)
    elif isinstance(target, set):
        target.add(value)
    else:
        raise NotImplementedError(f"add_to_collection is not supporting target type {type(target)}")


def find_non_none(_object):
    for value in _object:
        if value is not None:
            return value
    return None  # this statement can be removed


if __name__ == "__name__":
    raise NotImplementedError()
