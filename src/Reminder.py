"""
A class representing a reminder, which is a specialized calendar item.

Attributes
----------
priority : int
    The priority level of the reminder.
startDateComponents : object
    Components indicating when the reminder is to start.
dueDateComponents : object
    Components indicating when the reminder is due.
completed : bool
    Indicates if the reminder is completed.
completionDate : object
    The date when the reminder was completed.
recurrenceRules : list
    A list of rules defining how the reminder repeats.
"""

import json

from CalendarItem import CalendarItem


class Reminder(CalendarItem):
    def __init__(
        self,
        title="",
        calendar=None,
        notes="",
        creationDate=None,
        lastModifiedDate=None,
        URL="",
        priority=0,
        startDateComponents=None,
        dueDateComponents=None,
        completed=False,
        completionDate=None,
        recurrenceRules=None,
    ):
        super().__init__(title, calendar, notes, creationDate, lastModifiedDate, URL)
        self.priority = priority
        self.startDateComponents = startDateComponents
        self.dueDateComponents = dueDateComponents
        self.completed = completed
        self.completionDate = completionDate
        self.recurrenceRules = recurrenceRules if recurrenceRules is not None else []

    def _serialize_date_components(self, comp):
        """
        Helper method to serialize NSDateComponents into a dictionary.

        Parameters
        ----------
        comp : object
            An NSDateComponents instance.

        Returns
        -------
        dict or None
            A dictionary representation with keys like "year", "month", "day", "hour", "minute", "second",
            or None if comp is None.
        """

        # TODO: Handle time zones

        if comp is None:
            return None
        # Attempt to extract common components. If the method doesn't exist, default to None.
        try:
            d = {
                "year": comp.year() if hasattr(comp, "year") else None,
                "month": comp.month() if hasattr(comp, "month") else None,
                "day": comp.day() if hasattr(comp, "day") else None,
                "hour": comp.hour() if hasattr(comp, "hour") else None,
                "minute": comp.minute() if hasattr(comp, "minute") else None,
                "second": comp.second() if hasattr(comp, "second") else None,
            }
            # Remove keys with None values.
            return {k: v for k, v in d.items() if v is not None}
        except Exception:
            return str(comp)

    def to_dict(self):
        """
        Convert the Reminder object to a dictionary.

        Returns
        -------
        dict
            A dictionary representation of the Reminder.
        """
        base_dict = super().to_dict()
        base_dict.update(
            {
                "priority": self.priority,
                "startDateComponents": self._serialize_date_components(
                    self.startDateComponents
                ),
                "dueDateComponents": self._serialize_date_components(
                    self.dueDateComponents
                ),
                "completed": self.completed,
                "completionDate": (
                    str(self.completionDate) if self.completionDate else None
                ),
                "recurrenceRules": self.recurrenceRules,
            }
        )
        return base_dict

    def to_json(self):
        """
        Convert the Reminder object to a JSON string.

        Returns
        -------
        str
            A JSON-formatted string representing the Reminder.
        """
        return json.dumps(self.to_dict(), indent=4)

    def to_markdown(self):
        """
        Convert the Reminder object to a Markdown formatted string.

        Returns
        -------
        str
            A Markdown formatted string representing the Reminder.
        """
        d = self.to_dict()
        md_lines = ["### Reminder", ""]
        for key, value in d.items():
            md_lines.append(f"- **{key}**: {value}")
        return "\n".join(md_lines)

    def __str__(self):
        return (
            f"Reminder(title={self.title}, priority={self.priority}, "
            f"completed={self.completed}, dueDateComponents={self.dueDateComponents})"
        )
