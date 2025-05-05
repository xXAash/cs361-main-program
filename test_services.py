# test_services.py
# Comprehensive unit tests for student calendar project
# Covers assignment, class, event, and recurring functionality using the actual pipeline

import os
import subprocess
import pytest

# File paths
VIEW_FILE = "shared-files/view-request.txt"
INPUT_FILE = "shared-files/input.txt"
ASSIGNMENTS_FILE = "shared-files/assignments.txt"
SCHEDULE_FILE = "shared-files/schedule.txt"
OUTPUT_FILE = "shared-files/dashboard-output.txt"

# Utility: Clean and prepare shared-files directory before each test session
@pytest.fixture(autouse=True)
def clean_shared_files():
    os.makedirs("shared-files", exist_ok=True)
    for file in [INPUT_FILE, VIEW_FILE, ASSIGNMENTS_FILE, SCHEDULE_FILE, OUTPUT_FILE]:
        with open(file, "w") as f:
            f.truncate(0)

# Utility: Run a service script
def run_script(path):
    subprocess.run(["python", path], check=True)

# Utility: Read all output lines
def get_output():
    with open(OUTPUT_FILE) as f:
        return f.read()

# 1. Test basic assignment
def test_assignment_entry():
    with open(INPUT_FILE, "w") as f:
        f.write("type:assignment | title:HW1 | class:CS 361 | due_date:2025-05-07 | due_time:23:59\n")

    run_script("services/assignment_service.py")

    with open(ASSIGNMENTS_FILE) as f:
        content = f.read()
        assert "HW1" in content

# 2. Test basic class with location
def test_class_entry():
    with open(INPUT_FILE, "w") as f:
        f.write("type:class | title:CS361 | date:2025-05-07 | start_time:10:00 | end_time:11:30 | location:Kelley\n")

    run_script("services/class_event_service.py")

    with open(SCHEDULE_FILE) as f:
        content = f.read()
        assert "CS361" in content
        assert "Kelley" in content

# 3. Test event with no location
def test_event_no_location():
    with open(INPUT_FILE, "w") as f:
        f.write("type:event | title:Gym | date:2025-05-07 | start_time:15:00 | end_time:16:00\n")

    run_script("services/class_event_service.py")

    with open(SCHEDULE_FILE) as f:
        content = f.read()
        assert "Gym" in content
        assert "location" not in content.lower()

# 4. Test recurring class
def test_recurring_class():
    with open(INPUT_FILE, "w") as f:
        f.write("type:class | title:Math 251 | start_date:2025-05-01 | end_date:2025-05-08 | recurring_days:Wed | start_time:08:00 | end_time:09:00 | recurring:true\n")

    run_script("services/class_event_service.py")

    with open(SCHEDULE_FILE) as f:
        content = f.read()
        assert "Math 251" in content
        assert "2025-05-07" in content

# 5. Test recurring event
def test_recurring_event():
    with open(INPUT_FILE, "w") as f:
        f.write("type:event | title:Work | start_date:2025-05-01 | end_date:2025-05-10 | recurring_days:Wed | start_time:14:00 | end_time:17:00 | recurring:true\n")

    run_script("services/class_event_service.py")

    with open(SCHEDULE_FILE) as f:
        content = f.read()
        assert "Work" in content
        assert "2025-05-07" in content

# 6. Test daily view aggregates everything
def test_daily_view_combines_all():
    # Write matching date
    with open(VIEW_FILE, "w") as f:
        f.write("date:2025-05-07")

    # Write assignment, class, and event
    with open(ASSIGNMENTS_FILE, "w") as f:
        f.write("type:assignment | title:HW2 | class:CS340 | due_date:2025-05-07 | due_time:09:00\n")

    with open(SCHEDULE_FILE, "w") as f:
        f.write("type:class | title:CS340 | date:2025-05-07 | start_time:08:00 | end_time:09:50\n")
        f.write("type:event | title:Coffee Chat | date:2025-05-07 | start_time:10:00 | end_time:11:00\n")

    run_script("services/daily_view_service.py")

    out = get_output()
    assert "HW2" in out
    assert "CS340" in out
    assert "Coffee Chat" in out