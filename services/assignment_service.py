# ----------------------------------------------------------------------
# This file is part of the student-calendar project.
# It is used to process assignment entries from input.txt and store
# them in assignments.txt. Only entries of type:assignment are handled.
# ----------------------------------------------------------------------

# Import necessary library
import os

# ----------------------------------------------------------------------
# File paths used by this microservice
INPUT_FILE = "shared-files/input.txt"          # Where new entries are submitted
ASSIGNMENTS_FILE = "shared-files/assignments.txt"  # Where assignments are stored

# ----------------------------------------------------------------------

def process_line(line):
    """
    Parses a raw input line into a dictionary of key:value pairs.
    Format expected: key1:value1 | key2:value2 | ...
    Malformed segments are ignored.
    """
    parts = [part.strip() for part in line.split("|")]  # Clean up each segment
    return {
        kv.split(":", 1)[0]: kv.split(":", 1)[1]         # Split on first colon only
        for kv in parts if ":" in kv                     # Skip any malformed parts
    }

# ----------------------------------------------------------------------

def append_to_assignments(entry, original_line):
    """
    Appends the original input line (raw string) to assignments.txt.
    This is done for valid entries of type:assignment only.
    """
    with open(ASSIGNMENTS_FILE, "a") as f:
        f.write(original_line)  # Preserve the full line as-is

# ----------------------------------------------------------------------

def process_input():
    """
    Reads input.txt and processes assignment-type entries.
    - Moves assignment entries to assignments.txt
    - Preserves non-assignment entries and writes them back to input.txt
    """
    if not os.path.exists(INPUT_FILE):
        print("No input file found.")
        return

    # Read all input entries into memory
    with open(INPUT_FILE, "r") as f:
        lines = f.readlines()

    remaining_lines = []  # Keep entries that aren't assignments

    for line in lines:
        if "type:assignment" in line:
            entry = process_line(line)                    # Parse the assignment
            append_to_assignments(entry, line)            # Save it to file
            print(f"Processed: assignment - {entry.get('title', 'No title')}")
        else:
            remaining_lines.append(line)                  # Keep non-assignments for later

    # Rewrite input.txt with non-assignment entries only
    with open(INPUT_FILE, "w") as f:
        f.writelines(remaining_lines)

# ----------------------------------------------------------------------

# Entry point to run the service
if __name__ == "__main__":
    process_input()
