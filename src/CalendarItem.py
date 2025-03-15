"""
A base class representing a generic calendar item.

Attributes
----------
title : str
    The text describing the item.
calendar : str or object
    The calendar to which the item belongs.
notes : str
    Additional notes for the item.
creationDate : object
    The date the item was created.
lastModifiedDate : object
    The date the item was last modified.
URL : str
    An optional URL associated with the item.
startDate : object
    The start date (for events).
endDate : object
    The end date (for events).
"""

import json


class CalendarItem:
    def __init__(
        self,
        title="",
        calendar=None,
        notes="",
        creationDate=None,
        lastModifiedDate=None,
        URL="",
    ):
        self.title = title
        self.calendar = calendar
        self.notes = notes
        self.creationDate = creationDate
        self.lastModifiedDate = lastModifiedDate
        self.URL = URL
        # For events, add startDate and endDate attributes
        self.startDate = None
        self.endDate = None

    def to_dict(self):
        """
        Convert the CalendarItem object to a dictionary.

        Returns
        -------
        dict
            A dictionary representation of the CalendarItem.
        """
        return {
            "title": self.title,
            "calendar": (str(self.calendar.title()) if self.calendar else None),
            "notes": self.notes,
            "creationDate": str(self.creationDate) if self.creationDate else None,
            "lastModifiedDate": (
                str(self.lastModifiedDate) if self.lastModifiedDate else None
            ),
            "URL": self.URL,
            "startDate": str(self.startDate) if self.startDate else None,
            "endDate": str(self.endDate) if self.endDate else None,
        }

    def to_json(self):
        """
        Convert the CalendarItem object to a JSON string.

        Returns
        -------
        str
            A JSON-formatted string representing the CalendarItem.
        """
        return json.dumps(self.to_dict(), indent=4)

    def to_markdown(self):
        """
        Convert the CalendarItem object to a Markdown formatted string.

        Returns
        -------
        str
            A Markdown formatted string representing the CalendarItem.
        """
        d = self.to_dict()
        md_lines = ["### Calendar Item", ""]
        for key, value in d.items():
            md_lines.append(f"- **{key}**: {value}")
        return "\n".join(md_lines)

    def __str__(self):
        return f"CalendarItem(title={self.title}, calendar={self.calendar}, notes={self.notes})"
