# ----------------------------------------------------------------------
# This file is part of the student-calendar project.
# It is used to generate a combined view of assignments, one-time events, 
# and recurring events for a specific day.
# Output is written to dashboard-output.txt for frontend display.
# ----------------------------------------------------------------------

# Import necessary libraries
import os
import subprocess
from datetime import datetime

# File paths used by this service
VIEW_REQUEST_FILE = "shared-files/view-request.txt"
ASSIGNMENTS_FILE = "shared-files/assignments.txt"
SCHEDULE_FILE = "shared-files/schedule.txt"
DASHBOARD_OUTPUT_FILE = "shared-files/dashboard-output.txt"

# ----------------------------------------------------------------------

def process_line(line):
    """
    Parses a line into a dictionary of key:value pairs.
    Expects the format: key1:value1 | key2:value2 | ...
    """
    parts = [part.strip() for part in line.split("|")]
    return {
        kv.split(":", 1)[0]: kv.split(":", 1)[1]
        for kv in parts if ":" in kv
    }

# ----------------------------------------------------------------------

def process_view_request():
    """
    Generates a daily dashboard view by:
    1. Reading the target date from view-request.txt
    2. Collecting all assignments due that day
    3. Collecting all one-time and recurring events scheduled for that day
    4. Writing the final combined results to dashboard-output.txt
    """
    if not os.path.exists(VIEW_REQUEST_FILE):
        print("No view-request.txt file found.")
        return

    # 1. Read the view request line (e.g., "date:2025-05-07")
    with open(VIEW_REQUEST_FILE, "r") as f:
        request_line = f.readline().strip()

    # Parse the request into a dictionary
    request_parts = process_line(request_line)
    target_date = request_parts.get("date")

    if not target_date:
        print("Missing date in request.")
        return

    results = []  # Store matching entries for the target date

    # 2. Filter assignments that match the selected date
    if os.path.exists(ASSIGNMENTS_FILE):
        with open(ASSIGNMENTS_FILE, "r") as f:
            for line in f:
                entry = process_line(line)
                # Match if due_date exactly equals the requested date
                if entry.get("due_date") == target_date:
                    results.append(line)

    # 3. Filter one-time and recurring events that occur on that date
    if os.path.exists(SCHEDULE_FILE):
        with open(SCHEDULE_FILE, "r") as f:
            for line in f:
                entry = process_line(line)
                # Match by date field in schedule.txt
                if entry.get("date") == target_date:
                    results.append(line)

    # 4. Write all matching entries into dashboard-output.txt
    with open(DASHBOARD_OUTPUT_FILE, "w") as f:
        f.writelines(results)

    # Log how many results were found
    print(f"Combined view generated for {target_date} with {len(results)} result(s).")

# ----------------------------------------------------------------------

# Main entry point: Only runs if script is called directly
if __name__ == "__main__":
    process_view_request()
