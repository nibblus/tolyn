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

from time import sleep
from data.stopwatch import Stopwatch


def print_sleep(delay: float = 1, func=print):
    """
    Print a message and sleep
    :param delay: number of seconds to sleep
    :param func: method to use as output
    """
    func(f"Sleeping {delay} second(s).")
    sleep(delay)


print("Simple stopwatch")
sw = Stopwatch()
print(f"New stopwatch {sw}")
print_sleep(2)
sw.click_stop()
print(sw)

sw = Stopwatch(pattern="%a %Y-%m-%d %H:%M:%S:%f")
print_sleep(2)
sw.click_lap("Now ends the first lap")
print_sleep(1)
sw.click_lap("Now end is the second lap")
print(sw)
