# ----------------------------------------------------------------------
# This file is part of the student-calendar project.
# It is used to process class and event entries from input.txt
# and store them in schedule.txt. Other types are left untouched.
# ----------------------------------------------------------------------

# Import necessary library
import os
from datetime import datetime, timedelta

# File paths used by this microservice
INPUT_FILE = "shared-files/input.txt"
SCHEDULE_FILE = "shared-files/schedule.txt"

# ----------------------------------------------------------------------

def process_line(line):
    """
    Parses a single line from input.txt into a dictionary of key-value pairs.
    Format expected: key1:value1 | key2:value2 | ...
    Malformed segments are ignored.
    """
    # Split line by '|' and strip whitespace
    parts = [part.strip() for part in line.split("|")]

    # Create key:value dictionary from valid segments
    return {
        kv.split(":", 1)[0]: kv.split(":", 1)[1]
        for kv in parts if ":" in kv
    }

# ----------------------------------------------------------------------

def append_to_schedule(entry, original_line):
    """
    Appends a class or event entry to schedule.txt.
    The original input line is stored without modification.
    """
    with open(SCHEDULE_FILE, "a") as f:
        f.write(original_line)

# ----------------------------------------------------------------------

def process_input():
    # Ensure the input file exists before proceeding
    if not os.path.exists(INPUT_FILE):
        print("No input file found.")
        return

    # Read all entries from input.txt
    with open(INPUT_FILE, "r") as f:
        lines = f.readlines()

    remaining_lines = []  # Will store entries not processed (non-class/event)

    for line in lines:
        if "type:class" in line or "type:event" in line:
            entry = process_line(line)

            # -------------------------
            # Handle recurring entries
            # -------------------------
            if entry.get("recurring", "false").lower() == "true":
                start_date = entry.get("start_date")
                end_date = entry.get("end_date")
                recurring_days = entry.get("recurring_days", "")

                # Skip if recurrence fields are incomplete
                if not start_date or not end_date or not recurring_days:
                    print(f"Missing recurrence info for: {entry}")
                    continue

                # Create set of days to repeat on (e.g., {"Mon", "Wed"})
                days = set(day.strip() for day in recurring_days.split(","))

                # Convert start/end dates into datetime objects
                current = datetime.strptime(start_date, "%Y-%m-%d")
                end = datetime.strptime(end_date, "%Y-%m-%d")

                # Loop through each day in the date range
                while current <= end:
                    weekday = current.strftime("%a")  # Get day name like "Mon"
                    if weekday in days:
                        # Build a new entry line with the current date
                        new_line_parts = []
                        for key, value in entry.items():
                            if key not in {"recurring", "start_date", "end_date", "recurring_days"}:
                                new_line_parts.append(f"{key}:{value}")
                        new_line_parts.append(f"date:{current.strftime('%Y-%m-%d')}")

                        # Join parts into formatted line
                        new_line = " | ".join(new_line_parts) + "\n"
                        append_to_schedule(entry, new_line)
                    current += timedelta(days=1)  # Move to the next day

            else:
                # If not recurring, simply append the original entry
                append_to_schedule(entry, line)

            print(f"Processed: {entry['type']} - {entry.get('title', 'No title')}")

        else:
            # Non-class/event entries are kept for later processing
            remaining_lines.append(line)

    # Write unprocessed lines back to input.txt
    with open(INPUT_FILE, "w") as f:
        f.writelines(remaining_lines)

# ----------------------------------------------------------------------

# Entry point for script execution
if __name__ == "__main__":
    process_input()
