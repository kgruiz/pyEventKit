import objc
from EventKit import EKEvent, EKEventStore
from Foundation import NSDate

from CalendarItem import CalendarItem


def AddEvent(calendarItem: CalendarItem):
    """
    Creates and adds a new calendar event using EventKit based on a Python CalendarItem object.

    Parameters
    ----------
    calendarItem : CalendarItem
        A Python CalendarItem object that must have attributes `title`, `startDate`, and `endDate`.

    Returns
    -------
    CalendarItem
        The updated CalendarItem object with `creationDate`, `lastModifiedDate`, and `URL` set.

    Raises
    ------
    Exception
        If the event cannot be saved.
    """
    eventStore = EKEventStore.alloc().init()
    nativeEvent = EKEvent.eventWithEventStore_(eventStore)
    nativeEvent.setTitle_(calendarItem.title)
    nativeEvent.setStartDate_(calendarItem.startDate)
    nativeEvent.setEndDate_(calendarItem.endDate)

    if not calendarItem.calendar:
        calendarItem.calendar = eventStore.defaultCalendarForNewEvents()
    nativeEvent.setCalendar_(calendarItem.calendar)

    # Optional: set notes if available
    if hasattr(calendarItem, "notes") and calendarItem.notes:
        nativeEvent.setNotes_(calendarItem.notes)

    success, error = eventStore.saveEvent_span_error_(nativeEvent, 0, None)
    if not success:
        raise Exception("Failed to save event: " + error.localizedDescription())

    calendarItem.creationDate = nativeEvent.creationDate()
    calendarItem.lastModifiedDate = nativeEvent.lastModifiedDate()
    calendarItem.URL = nativeEvent.URL()

    return calendarItem
