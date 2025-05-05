# ----------------------------------------------------------------------
# This file is part of the student-calendar project.
# It is used to serve the main Flask API for routing requests from the frontend,
# triggering microservices, and handling shared-file communication.
# -----------------------------------------------------------------------

# Import necessary libraries
from flask import Flask, request, send_from_directory
import os
import subprocess

# Initialize Flask app
app = Flask(__name__)

# Define the directory for shared files (.txt files for communication between services)
SHARED_DIR = "shared-files"

# -----------------------------------------------------------------------

@app.route("/write-view-request", methods=["POST"])
def write_view_request():
    """
    Handles POST requests from the frontend to update the view.
    Writes the requested date to view-request.txt and runs the view service.
    """
    content = request.data.decode("utf-8")  # Decode raw text from frontend

    # Write the content (e.g., "date:2025-05-05") into view-request.txt
    with open(os.path.join(SHARED_DIR, "view-request.txt"), "w") as f:
        f.write(content)

    # Run the daily view service script to process the request
    subprocess.run(["python", "services/daily_view_service.py"])
    
    # Respond with success
    return "Request written and view processed", 200

# -----------------------------------------------------------------------

@app.route("/run-script", methods=["POST"])
def run_script():
    """
    Executes a service script based on the script path received in the request.
    Typically used to run assignment_service.py or class_event_service.py.
    """
    import json
    data = json.loads(request.data)            # Parse incoming JSON payload
    script_path = data.get("script")           # Get the script path from the JSON

    # If no script provided or file doesn't exist, return error
    if not script_path or not os.path.exists(script_path):
        return "Script not found", 400

    # Execute the provided Python script
    subprocess.run(["python", script_path])

    # Return success response
    return "Script executed", 200

# -----------------------------------------------------------------------

@app.route("/dashboard-output.txt", methods=["GET"])
def get_dashboard_output():
    """
    Sends the dashboard-output.txt file to the frontend.
    This file includes the list of assignments, classes, and events for a selected date.
    """
    return send_from_directory(SHARED_DIR, "dashboard-output.txt")

# -----------------------------------------------------------------------

@app.route("/", defaults={"path": "index.html"})
@app.route("/<path:path>")
def serve_frontend(path):
    """
    Serves static frontend files (HTML, JS, CSS) from the 'frontend' folder.
    """
    return send_from_directory("frontend", path)

# -----------------------------------------------------------------------

@app.route("/submit-entry", methods=["POST"])
def submit_entry():
    """
    Appends a raw user entry (assignment, class, or event) to input.txt.
    This line will later be picked up by a microservice for processing.
    """
    content = request.data.decode("utf-8")     # Get raw text from frontend form
    print("Incoming entry:", content)          # Log it to server console for debugging

    # Append the line to input.txt (adding a newline after)
    with open(os.path.join(SHARED_DIR, "input.txt"), "a") as f:
        f.write(content + "\n")

    # Confirm entry was received
    return "Entry written to input.txt", 200

# -----------------------------------------------------------------------

@app.post("/clear-all")
def clear_all_data():
    '''
    Clears all data files by overwriting them with empty strings.
    This is used for the Clear All Data button in the frontend.
    '''

    # Paths to your data files
    files_to_clear = [
        "shared-files/assignments.txt",
        "shared-files/input.txt",
        "shared-files/schedule.txt",
        "shared-files/dashboard-output.txt"
    ]

    for file_path in files_to_clear:
        try:
            with open(file_path, "w") as f:
                f.write("")  # Overwrite file with empty string
        except FileNotFoundError:
            pass  # It's okay if the file doesn't exist yet

    return {"status": "cleared"}

# -----------------------------------------------------------------------

# Start the Flask development server when running this script directly
if __name__ == "__main__":
    app.run(debug=True)  # Enable debug mode for easier development