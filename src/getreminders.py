import time

import objc
from EventKit import EKEntityTypeReminder, EKEventStore
from Foundation import NSDate, NSRunLoop

from Reminder import Reminder


def GetReminders() -> list[Reminder]:
    """
    Retrieves reminders via EventKit and returns them as Python Reminder objects.

    Returns
    -------
    list of Reminder
        A list of Reminder objects.

    Notes
    -----
    Uses the run loop to wait for the asynchronous callback.
    """
    eventStore = EKEventStore.alloc().init()
    nativeReminders = []
    finished = [False]

    def callback(reminders):
        nonlocal nativeReminders
        nativeReminders = reminders if reminders is not None else []
        finished[0] = True

    predicate = eventStore.predicateForRemindersInCalendars_(None)
    eventStore.fetchRemindersMatchingPredicate_completion_(predicate, callback)

    runLoop = NSRunLoop.currentRunLoop()
    timeout = time.time() + 5.0
    while not finished[0] and time.time() < timeout:
        runLoop.runUntilDate_(NSDate.dateWithTimeIntervalSinceNow_(0.1))

    pyReminders = []
    for nativeReminder in nativeReminders:
        r = Reminder(
            title=nativeReminder.title(),
            calendar=nativeReminder.calendar(),
            notes=(nativeReminder.notes() if hasattr(nativeReminder, "notes") else ""),
            creationDate=nativeReminder.creationDate(),
            lastModifiedDate=nativeReminder.lastModifiedDate(),
            URL=nativeReminder.URL(),
            priority=(
                nativeReminder.priority() if hasattr(nativeReminder, "priority") else 0
            ),
            startDateComponents=nativeReminder.startDateComponents(),
            dueDateComponents=nativeReminder.dueDateComponents(),
            completed=nativeReminder.isCompleted(),  # Fixed: use isCompleted() instead of completed()
            completionDate=nativeReminder.completionDate(),
            recurrenceRules=(
                list(nativeReminder.recurrenceRules())
                if nativeReminder.recurrenceRules() is not None
                else []
            ),
        )
        pyReminders.append(r)

    return pyReminders
