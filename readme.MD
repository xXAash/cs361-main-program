# Student Calendar

This is a student-friendly calendar and scheduling app built using Python (Flask), HTML/CSS, JavaScript, and TailwindCSS. It allows users to manage their classes, assignments, and events.

## Features

- Add **Assignments**, **Classes**, and **Events**
- Support for **recurring classes/events**
- View a **daily dashboard** with:
  - Date picker (5-day scroll)
  - Schedule of events/classes
  - Assignments due
- Microservice-based architecture using `.txt` file communication
- Fully styled UI using TailwindCSS

## Project Structure

student-calendar/
├── frontend/
│ ├── index.html
│ └── main.js
├── services/
│ ├── assignment_service.py
│ ├── class_event_service.py
│ ├── recurring_service.py
│ └── daily_view_service.py
├── shared-files/
│ ├── input.txt
│ ├── assignments.txt
│ ├── schedule.txt
│ ├── view-request.txt
│ ├── dashboard-output.txt
│ └── recurring-output.txt
├── app.py
└── README.md

## Getting Started

1. Clone the repo:

   ```bash
   git clone https://github.com/xXAash/student-calendar.git
   cd student-calendar
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:

   ```bash
   python app.py
   ```

4. View the app:
   Open your browser to `http://localhost:5000`

## Tech Stack

- Frontend: HTML, TailwindCSS, JavaScript
- Backend: Python with Flask
- Storage: Plain `.txt` files (for microservice communication)
