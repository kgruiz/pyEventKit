import time

import objc
from EventKit import EKEntityTypeEvent, EKEventStore
from Foundation import NSCalendar, NSDate, NSDateComponents, NSRunLoop

from CalendarItem import CalendarItem


def GetEvents(startDate=None, endDate=None) -> list[CalendarItem]:
    """
    Retrieves calendar events via EventKit and returns them as Python CalendarItem objects.
    Defaults to now until one year from now.

    Parameters
    ----------
    startDate : NSDate, optional
        The start date (default is now).
    endDate : NSDate, optional
        The end date (default is one year from now).

    Returns
    -------
    list of CalendarItem
        A list of CalendarItem objects.
    """
    eventStore = EKEventStore.alloc().init()

    if startDate is None:
        startDate = NSDate.date()
    if endDate is None:
        calendar = NSCalendar.currentCalendar()
        components = NSDateComponents.alloc().init()
        components.setYear_(1)
        endDate = calendar.dateByAddingComponents_toDate_options_(
            components, NSDate.date(), 0
        )

    calendars = eventStore.calendarsForEntityType_(EKEntityTypeEvent)
    predicate = eventStore.predicateForEventsWithStartDate_endDate_calendars_(
        startDate, endDate, calendars
    )
    nativeEvents = eventStore.eventsMatchingPredicate_(predicate)

    pyEvents = []
    for nativeEvent in nativeEvents:
        item = CalendarItem(
            title=nativeEvent.title(),
            calendar=nativeEvent.calendar(),
            notes=(nativeEvent.notes() if hasattr(nativeEvent, "notes") else ""),
            creationDate=nativeEvent.creationDate(),
            lastModifiedDate=nativeEvent.lastModifiedDate(),
            URL=nativeEvent.URL(),
        )
        item.startDate = nativeEvent.startDate()
        item.endDate = nativeEvent.endDate()
        pyEvents.append(item)

    return pyEvents
