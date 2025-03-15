import datetime

import objc
from EventKit import EKEventStore, EKReminder
from Foundation import NSCalendar, NSDate

from Reminder import Reminder


def AddReminder(reminder: Reminder):
    """
    Creates and adds a new reminder using EventKit based on a Python Reminder object.

    Parameters
    ----------
    reminder : Reminder
        A Python Reminder object that should have attribute `title` and optionally a `dueDate` (as Python datetime)
        or `dueDateComponents`.

    Returns
    -------
    Reminder
        The updated Python Reminder object with `creationDate` and `lastModifiedDate` set.

    Raises
    ------
    Exception
        If the reminder cannot be saved.
    """
    eventStore = EKEventStore.alloc().init()
    nativeReminder = EKReminder.reminderWithEventStore_(eventStore)
    nativeReminder.setTitle_(reminder.title)

    if not reminder.calendar:
        reminder.calendar = eventStore.defaultCalendarForNewReminders()
    nativeReminder.setCalendar_(reminder.calendar)

    if hasattr(reminder, "notes") and reminder.notes:
        nativeReminder.setNotes_(reminder.notes)

    # If the Python object has a dueDate attribute (a Python datetime), use it.
    if hasattr(reminder, "dueDate") and reminder.dueDate is not None:
        nsDueDate = NSDate.dateWithTimeIntervalSince1970_(reminder.dueDate.timestamp())
        calendarObj = NSCalendar.currentCalendar()
        NSCalendarUnitYear = 1 << 11
        NSCalendarUnitMonth = 1 << 12
        NSCalendarUnitDay = 1 << 13
        units = NSCalendarUnitYear | NSCalendarUnitMonth | NSCalendarUnitDay
        components = calendarObj.components_fromDate_(units, nsDueDate)
        nativeReminder.setDueDateComponents_(components)
    elif hasattr(reminder, "dueDateComponents") and reminder.dueDateComponents:
        nativeReminder.setDueDateComponents_(reminder.dueDateComponents)

    success, error = eventStore.saveReminder_commit_error_(nativeReminder, True, None)
    if not success:
        raise Exception("Failed to save reminder: " + error.localizedDescription())

    reminder.creationDate = nativeReminder.creationDate()
    reminder.lastModifiedDate = nativeReminder.lastModifiedDate()
    return reminder
