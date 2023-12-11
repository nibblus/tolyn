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


def _method_text(method_name: str)-> str:
    return "" if method_name is None else f" of method {method_name}"


def _domain_text(domain):
    return "" if domain is None else f" Allowed values: {domain}"


def error_param_value_invalid(param_name:str, value=object, method_name= None, domain = None) -> str:
    """
    Generate an error message specific for invalid values in method parameters
    :param param_name: Parameter name
    :param value: Parameter value
    :param method_name: Method name
    :param domain: Accepted values
    :return: error message
    """
    return f"Parameter {param_name}{_method_text(method_name)} has invalid value {value}.{_domain_text(_domain)}"


def error_param_value_none(param_name:str, method_name= None, domain = None) -> str:
    """
    Generate an error message specific for invalid values in method parameters
    :param param_name: Parameter name
    :param value: Parameter value
    :param method_name: Method name
    :param accepted_values: Accepted values
    :return: error message
    """
    return f"Parameter {param_name}{_method_text(method_name)} is None.{_domain_text(domain)}"



def block_header(message: str = "", pre_blanks: int = 0, post_blanks: int = 0, char: str = "-", newline: str = os.linesep, width: int = 255) -> str:
    """
    Create a header
    :param message: text to output
    :param pre_blanks: number of empty lines in front of message
    :param post_blanks: number of empty line after message
    :param char: filler character
    :param newline: newline str
    :param width: line width
    """
    ret = []
    for i in range(pre_blanks):
        ret.append('')
    ret.append(char * width)
    ret.append(f"{char * 2} {message}")
    ret.append(char * width)

    for i in range(post_blanks):
        ret.append('')
    return newline.join(ret)


if __name__ == "__main__":
    print(block_header("hallo", 2, 2, '*-', width=50))
    raise NotImplementedError()
