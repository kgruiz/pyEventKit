import datetime
import json

from Foundation import NSDate

from addevent import AddEvent
from addreminder import AddReminder
from CalendarItem import CalendarItem
from getevents import GetEvents
from getreminders import GetReminders
from Reminder import Reminder


def SaveToFile(fileName, content):
    """
    Save content to a file.

    Parameters
    ----------
    fileName : str
        The name of the file to save content to.
    content : str
        The content to be written to the file.
    """
    with open(fileName, "w", encoding="utf-8") as file:
        file.write(content)
    print(f"Saved {fileName}")


def ExampleAddEvent():
    """
    Add an event and save JSON and Markdown representations to files.
    """
    startDate = NSDate.date()
    endDate = NSDate.dateWithTimeIntervalSinceNow_(3600)  # 1 hour later
    eventItem = CalendarItem(title="Example Event")
    eventItem.startDate = startDate
    eventItem.endDate = endDate

    try:
        event = AddEvent(eventItem)
        print("Added event:", event.title)

        # Save event to files
        SaveToFile("event.json", event.to_json())
        SaveToFile("event.md", event.to_markdown())

    except Exception as ex:
        print("Error adding event:", ex)


def ExampleGetEvents():
    """
    Retrieve events and save JSON and Markdown representations to files.
    """
    events = GetEvents()
    allEventsJson = [event.to_dict() for event in events]
    allEventsMarkdown = "\n\n".join(event.to_markdown() for event in events)

    # Save to files
    SaveToFile("events.json", json.dumps(allEventsJson, indent=4))
    SaveToFile("events.md", allEventsMarkdown)

    for event in events:
        print("Event:", event.title, event.startDate)


def ExampleAddReminder():
    """
    Add a reminder and save JSON and Markdown representations to files.
    """
    dueDate = datetime.datetime.now() + datetime.timedelta(days=1)
    reminderItem = Reminder(title="Example Reminder")
    reminderItem.dueDate = dueDate

    try:
        updatedReminder = AddReminder(reminderItem)
        print("Added reminder:", updatedReminder.title)

        # Save reminder to files
        SaveToFile("reminder.json", updatedReminder.to_json())
        SaveToFile("reminder.md", updatedReminder.to_markdown())

    except Exception as ex:
        print("Error adding reminder:", ex)


def ExampleGetReminders():
    """
    Retrieve reminders and save JSON and Markdown representations to files.
    """
    reminders = GetReminders()
    allRemindersJson = [reminder.to_dict() for reminder in reminders]
    allRemindersMarkdown = "\n\n".join(reminder.to_markdown() for reminder in reminders)

    # Save to files
    SaveToFile("reminders.json", json.dumps(allRemindersJson, indent=4))
    SaveToFile("reminders.md", allRemindersMarkdown)

    for reminder in reminders:
        print("Reminder:", reminder.title)


if __name__ == "__main__":
    # Uncomment the examples you want to run:
    # ExampleAddEvent()
    # ExampleGetEvents()
    # ExampleAddReminder()
    ExampleGetReminders()
