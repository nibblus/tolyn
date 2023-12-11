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

from datetime import datetime

import os


class StopwatchError(Exception):
    """
    Specific Error for stopwatch functionality
    """
    pass


class Lap:
    """
    Lap, like on a stopwatch
    """

    def __init__(self, base: datetime, previous: datetime, start: datetime, name: str = "", pattern: str = "%x %X") -> None:
        self.base = base
        self.previous = previous
        self.start = start
        self.elapsed_since_start = start - base
        self.elapsed_since_previous = start - previous
        self.name = name
        self.pattern = pattern

    def __repr__(self) -> str:
        name_text = '' if self.name is None or len(self.name) == 0 else f"'{self.name}'"
        return f"LAP {name_text:30}' clicked at {self.start.strftime(self.pattern)}, absolute {self.elapsed_since_start.strftime(self.pattern)}, relative: {self.elapsed_since_previous.strftime(self.pattern)}"

    def indented_repr(self, indent: int) -> str:
        """
        Right alignment indent
        :param indent: number of characters
        """
        return f"LAP '{self.name:{indent}}' clicked at {self.start}, absolute {self.elapsed_since_start}, relative: {self.elapsed_since_previous}"


class Stopwatch:
    """
    Basic stopwatch functionality to measure time with intermediate intervals
    A stopwatch has three buttons:
    - START: resets the watch (start time and laps) and starts running
    -  STOP: stop the watch
    -   LAP: which stores an intermediate interval
    """

    # TODO: If START is clicked after STOP then the stopwatch should leave a gap in the laps.

    def __init__(self, align: bool = True, pattern: str = "%x %X") -> None:
        """
        Initialize the stopwatch:
        - start time is set to now
        - laps are emptied
        :param align: If True laps: When printing all laps, the names will be right-filled with spaces until all names have the same length. Otherwise, the lap names will be printed as-is
        :param pattern: timestamp format, see datetime.strftime()
        """
        self.start = self.previous = datetime.now()  # start time, time of the previous click on 'LAP'
        self.stop = None  # if a stopwatch has been stopped, no further clicks are allowed
        self.laps = []
        self.align = align
        self.pattern = pattern

    def __repr__(self) -> str:
        width = max([len(lap.name) for lap in self.laps] or [0]) if self.align else 0
        return os.linesep.join(self.lap_texts(width))

    def lap_texts(self, width: int = 0) -> list:
        """
        Create list of lap descriptions
        :param width: minimal width of the lap name
        """
        ret = [f"Stopwatch started at: {self.start.strftime(self.pattern)}"]
        for lap in self.laps:
            ret.append(f"{lap.indented_repr(width)}")
        if self.stop is not None:
            ret.append(f"stopped a {self.start.strftime(self.pattern)}")
        return ret

    def click_start(self) -> None:
        """
        Reset the stopwatch.
        """
        self.__init__()

    def click_lap(self, name: str = "", exact_time=None) -> None:
        """
        Click on the LAP button
        :param name: Name of the lap
        :param exact_time: Time to end the lap, if not provided 'now' will be used
        """
        click_time = datetime.now() if exact_time is None else exact_time
        if self.stop is not None:
            raise StopwatchError("Watch is already stopped. Can not add laps")
        self.laps.append(Lap(self.start, self.previous, click_time, name, self.pattern))
        self.previous = click_time

    def click_stop(self, name: str = ""):
        """
        Click on the STOP button
        """
        stop = datetime.now()
        self.click_lap(name, stop)
        self.stop = stop
        self.previous = None

    def html(self) -> str:
        """
        HTML representation of the stopwatch
        """
        return f"""{"<BR/>".join(self.lap_texts())}"""


if __name__ == "__main__":
    raise NotImplementedError(__file__)
