# -*- coding=utf-8 -*-
r"""

"""
import typing as t
from datetime import date
import pydantic


__all__ = ['DateRange']


OptionalDate: t.TypeAlias = t.Optional[date]
date_parser = pydantic.TypeAdapter(OptionalDate).validate_python


class DateRange(pydantic.BaseModel):
    start: t.Optional[date]
    end: t.Optional[date]

    @classmethod
    def from_string(cls, date_range: str) -> 'DateRange':
        r"""
        parses a string to a DateRange

        - `2000-01-01` (single date)
        - `2000-01-01:` (start without end)
        - `:2000-01-01` (end without start)
        - `2000-01-01:2001-01-01` (start and end)
        - `2001-01-01:2000-01-01` (automatically switched)

        :param date_range: string representing a date range
        :return: DateRange
        """
        start, sep, end = date_range.partition(":")
        if not sep:
            start_and_end = date_parser(date_range)
            return DateRange(start=start_and_end, end=start_and_end)
        else:
            start = date_parser(start) if start else None
            end = date_parser(end) if end else None
            if start is None or end is None:
                return DateRange(start=start, end=end)
            else:
                return DateRange(start=start, end=end) if start < end else DateRange(start=end, end=start)


if __name__ == '__main__':
    print(DateRange.from_string("2020-01-10"))
    print(DateRange.from_string("2020-01-10:"))
    print(DateRange.from_string(":2020-01-10"))
    print(DateRange.from_string("2019-01-01:2020-01-10"))
    print(DateRange.from_string("2020-01-01:2019-01-10"))
