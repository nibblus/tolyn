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

import datetime
import os


class Lap:
    """
    Lap, like on a stopwatch
    """

    def __init__(self, base, previous, start, name="") -> None:
        self.base = base
        self.previous = previous
        self.start = start
        self.elapsed_since_start = start - base
        self.elapsed_since_previous = start - previous
        self.name = name

    def __repr__(self) -> str:
        return f"LAP '{self.name:30}' clicked at {self.start}, absolute {self.elapsed_since_start}, relative: {self.elapsed_since_previous}"

    def indented_repr(self, indent: int) -> str:
        """
        Right alignment indent
        :param indent: number of characters
        """
        return f"LAP '{self.name:{indent}}' clicked at {self.start}, absolute {self.elapsed_since_start}, relative: {self.elapsed_since_previous}"


class Stopwatch:
    """
    Basic stopwatch functionality
    """

    def __init__(self) -> None:
        self.start = self.previous_click = datetime.datetime.now()
        self.laps = []

    def __str__(self) -> str:
        indent = max([len(lap.name) for lap in self.laps])
        return os.linesep.join(self.lap_list(indent))

    def lap_list(self, indent=0) -> list:
        """
        Create list of lap descriptions
        """
        ret = [f"Timer started at: {self.start}"]
        for lap in self.laps:
            ret.append(f"{lap.indented_repr(indent)}")
        return ret

    def html(self) -> str:
        """
        HTML representaion of the stopwatch
        """
        return f""" {"<BR/>".join(self.lap_list())}"""

    def click_start(self) -> None:
        """
        Reset the laps, set start time to now
        """
        self.start = self.previous_click = datetime.datetime.now()
        self.laps = []

    def click(self, name="") -> None:
        """
        Add a lap
        :param name: Optional name of the lap
        """
        new_click_time = datetime.datetime.now()
        lap = Lap(self.start, self.previous_click, new_click_time, name)
        self.laps.append(lap)
        self.previous_click = new_click_time


if __name__ == "__main__":
    raise NotImplementedError(__file__)
