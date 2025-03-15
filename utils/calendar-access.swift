import Foundation
import EventKit

/// Prints detailed information for an EventKit error.
/// It converts the error code to an EKError.Code and prints a human‐readable message.
func printDetailedEventKitError(_ error: Error?) {
    guard let nsError = error as NSError? else {
        print("No error information available.")
        return
    }

    print("Error Domain: \(nsError.domain)")
    print("Error Code: \(nsError.code)")
    print("Description: \(nsError.localizedDescription)")
    print("User Info: \(nsError.userInfo)")

    if nsError.domain == EKErrorDomain {
        if let ekErrorCode = EKError.Code(rawValue: nsError.code) {
            switch ekErrorCode {
            case .eventNotMutable:
                print("Detailed Info: The event isn't mutable and cannot be saved or deleted.")
            case .noCalendar:
                print("Detailed Info: The event isn't associated with any calendar.")
            case .noStartDate:
                print("Detailed Info: The event has no start date set.")
            case .noEndDate:
                print("Detailed Info: The event has no end date set.")
            case .datesInverted:
                print("Detailed Info: The event's end date occurs before its start date.")
            case .internalFailure:
                print("Detailed Info: An internal error occurred.")
            case .calendarReadOnly:
                print("Detailed Info: The calendar is read-only; events cannot be added.")
            case .eventStoreNotAuthorized:
                print("Detailed Info: The user hasn't authorized access to events or reminders.")
            default:
                print("Detailed Info: Unhandled EKError.Code: \(ekErrorCode)")
            }
        } else {
            print("Could not convert error code to EKError.Code.")
        }
    }
}

// Create an instance of EKEventStore
let eventStore = EKEventStore()

// Function to request calendar access, using new API on macOS 14+ if available.
func requestCalendarAccess(completion: @escaping (Bool, Error?) -> Void) {
    if #available(macOS 14, *) {
        eventStore.requestFullAccessToEvents { granted, error in
            completion(granted, error)
        }
    } else {
        eventStore.requestAccess(to: .event) { granted, error in
            completion(granted, error)
        }
    }
}

// Request access to the calendar.
requestCalendarAccess { granted, error in
    if granted {
        print("Calendar access granted!")

        // List available calendars.
        let calendars = eventStore.calendars(for: .event)
        print("Found \(calendars.count) calendar(s):")
        for calendar in calendars {
            print(" - \(calendar.title)")
        }

        // Try an EventKit operation that should trigger an error.
        // Here we intentionally create an event with missing required fields.
        let testEvent = EKEvent(eventStore: eventStore)
        testEvent.title = "Test Event"
        // Missing startDate and endDate to trigger an error.
        testEvent.calendar = eventStore.defaultCalendarForNewEvents

        do {
            try eventStore.save(testEvent, span: .thisEvent)
            print("Test event saved successfully!")
        } catch {
            print("Failed to save test event:")
            printDetailedEventKitError(error)
        }
    } else {
        print("Calendar access denied!")
        if let error = error {
            printDetailedEventKitError(error)
        } else {
            let status = EKEventStore.authorizationStatus(for: .event)
            print("No detailed error available. Current authorization status: \(status.rawValue)")
            // Handle all possible statuses, including new ones in macOS 14+
            switch status {
            case .denied:
                print("Access denied by the user.")
            case .restricted:
                print("Access restricted (parental controls or system policy).")
            case .notDetermined:
                print("Authorization not determined.")
            case .authorized:
                print("Access already granted.")
            case .fullAccess:
                print("Access granted with full access.")
            case .writeOnly:
                print("Access granted in write-only mode.")
            @unknown default:
                print("Unknown authorization status.")
            }
        }
    }
    exit(EXIT_SUCCESS)
}

// Keep the run loop running until the async callback completes.
RunLoop.main.run()
