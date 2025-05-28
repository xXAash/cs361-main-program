import { fetchClasses, fetchEvents, fetchTasks } from "../utils/api.js";
import { formatDate, formatTask, formatClassEvent } from "../utils/format.js";

export function updateViewRequest(userId, focusedDate, viewType = "daily") {
  const dateStr = formatDate(focusedDate);
  document.getElementById("current-date").textContent =
    focusedDate.toDateString();

  if (viewType !== "daily") {
    console.log(
      `View type '${viewType}' selected — waiting for backend support.`
    );
    // TODO: Replace with fetch to view microservice once implemented
    return;
  }

  const assignments = [];
  const schedule = [];

  Promise.all([
    fetchClasses(userId),
    fetchEvents(userId),
    fetchTasks(userId),
  ]).then(([classes, events, tasks]) => {
    const weekday = focusedDate.toLocaleDateString("en-US", {
      weekday: "long",
    });

    localStorage.setItem("user_classes", JSON.stringify(classes));
    localStorage.setItem("user_events", JSON.stringify(events));

    classes.forEach((cls) => {
      if (cls.class_date === dateStr || cls.days?.includes(weekday)) {
        schedule.push(formatClassEvent(cls));
      }
    });

    events.forEach((evt) => {
      if (
        (evt.event_date && evt.event_date === dateStr) ||
        (evt.recurring?.is_recurring &&
          evt.recurring.days.includes(weekday) &&
          evt.recurring.start_date <= dateStr &&
          evt.recurring.end_date >= dateStr)
      ) {
        schedule.push(formatClassEvent(evt));
      }
    });

    tasks.forEach((task) => {
      if (task.due_date === dateStr) {
        assignments.push(formatTask(task));
      }
    });

    document.getElementById("schedule-section").innerHTML = schedule
      .map(
        (s) => `<div class="bg-gray-100 px-3 py-2 rounded shadow-sm">${s}</div>`
      )
      .join("");

    document.getElementById("assignment-section").innerHTML = assignments
      .map(
        (a) => `<div class="bg-gray-100 px-3 py-2 rounded shadow-sm">${a}</div>`
      )
      .join("");
  });
}
