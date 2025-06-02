import {
  postTask,
  postClass,
  postRecurringClass,
  postEvent,
  postRecurringEvent,
} from "../utils/api.js";
import { updateViewRequest } from "./render.js";

export function openModal(type) {
  const modal = document.getElementById("modal-overlay");
  const form = document.getElementById("modal-form");
  const title = document.getElementById("modal-title");

  modal.classList.remove("hidden");
  form.innerHTML = "";
  form.dataset.type = type;

  if (type === "addTask") {
    title.textContent = "Add Task";
    renderTaskForm(form);
  } else if (type === "addClass") {
    title.textContent = "Add Class";
    renderClassForm(form);
  } else if (type === "addEvent") {
    title.textContent = "Add Event";
    renderEventForm(form);
  }
}

function renderTaskForm(form) {
  const classes = JSON.parse(localStorage.getItem("user_classes") || "[]");
  const events = JSON.parse(localStorage.getItem("user_events") || "[]");

  const uniqueClassTitles = [...new Set(classes.map((cls) => cls.title))];
  const uniqueEventTitles = [...new Set(events.map((evt) => evt.title))];

  const options = [
    ...uniqueClassTitles.map(
      (title) => `<option value="class::${title}">${title} (Class)</option>`
    ),
    ...uniqueEventTitles.map(
      (title) => `<option value="event::${title}">${title} (Event)</option>`
    ),
  ];

  form.innerHTML = `
    <input name="title" placeholder="Task Title" required class="w-full border px-2 py-1 rounded" />
    <input name="description" placeholder="Description" class="w-full border px-2 py-1 rounded" />
    <input name="due_date" type="date" required class="w-full border px-2 py-1 rounded" />
    <input name="due_time" type="time" required class="w-full border px-2 py-1 rounded" />
    <select name="linked_to" class="w-full border px-2 py-1 rounded">
      <option value="">-- Link to Class/Event (optional) --</option>
      ${options.join("")}
    </select>
  `;
}

function renderClassForm(form) {
  form.innerHTML = `
    <input name="title" placeholder="Class Title" required class="w-full border px-2 py-1 rounded" />
    <input name="location" placeholder="Location" required class="w-full border px-2 py-1 rounded" />

    <label class="block mt-2">
      <input type="checkbox" name="online" id="onlineCheckbox" class="mr-2" /> Online Class
    </label>

    <div id="offline-fields">
      <input name="room" placeholder="Room (optional)" class="w-full border px-2 py-1 rounded" />
      <div class="my-2">Time:</div>
      <div class="flex items-center gap-2 mb-2">
        <input name="start_time" type="time" required class="border px-2 py-1 rounded" />
        <span>–</span>
        <input name="end_time" type="time" required class="border px-2 py-1 rounded" />
      </div>
      <div class="my-2">Days:</div>
      <div class="flex flex-wrap gap-2 mb-2">
        ${["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
          .map(
            (day) =>
              `<label><input type="checkbox" name="days" value="${day}" class="mr-1" />${day}</label>`
          )
          .join("")}
      </div>
      <div class="mb-2">Term:</div>
      <div class="flex gap-2 mb-2">
        ${["fall", "winter", "spring", "summer"]
          .map(
            (term) =>
              `<label><input type="radio" name="term" value="${term}" class="mr-1" />${
                term[0].toUpperCase() + term.slice(1)
              }</label>`
          )
          .join("")}
      </div>
      <select name="year" class="w-full border px-2 py-1 rounded">
        ${Array.from({ length: 6 }, (_, i) => {
          const y = 2023 + i;
          return `<option value="${y}">${y}</option>`;
        }).join("")}
      </select>
    </div>
  `;

  const onlineCheckbox = document.getElementById("onlineCheckbox");
  const offlineFields = document.getElementById("offline-fields");

  onlineCheckbox.addEventListener("change", () => {
    offlineFields.style.display = onlineCheckbox.checked ? "none" : "block";
  });
}

function renderEventForm(form) {
  form.innerHTML = `
    <input name="title" placeholder="Event Title" required class="w-full border px-2 py-1 rounded" />
    <input name="location" placeholder="Location" required class="w-full border px-2 py-1 rounded" />

    <label class="block mt-2">
      <input type="checkbox" name="is_recurring" id="recurringCheckbox" class="mr-2" />
      Recurring Event?
    </label>

    <div id="date-fields">
      <input name="date" type="date" class="w-full border px-2 py-1 rounded" />
    </div>

    <div id="recurring-fields" style="display:none;">
      <div class="my-2 font-semibold">Recurring Days</div>
      <div class="flex flex-wrap gap-2 mb-2">
        ${[
          "Monday",
          "Tuesday",
          "Wednesday",
          "Thursday",
          "Friday",
          "Saturday",
          "Sunday",
        ]
          .map(
            (day) =>
              `<label><input type="checkbox" name="recurring_days" value="${day}" class="mr-1" />${day}</label>`
          )
          .join("")}
      </div>
      <input name="start_date" type="date" class="w-full border px-2 py-1 rounded" placeholder="Start Date" />
      <input name="end_date" type="date" class="w-full border px-2 py-1 rounded" placeholder="End Date" />
    </div>

    <div class="flex items-center gap-2 mb-2 mt-2">
      <input name="start_time" type="time" required class="border px-2 py-1 rounded" />
      <span>–</span>
      <input name="end_time" type="time" required class="border px-2 py-1 rounded" />
    </div>
  `;

  const checkbox = document.getElementById("recurringCheckbox");
  const dateFields = document.getElementById("date-fields");
  const recurringFields = document.getElementById("recurring-fields");

  checkbox.addEventListener("change", () => {
    if (checkbox.checked) {
      dateFields.style.display = "none";
      recurringFields.style.display = "block";
    } else {
      dateFields.style.display = "block";
      recurringFields.style.display = "none";
    }
  });
}

export function submitModal(userId, focusedDate) {
  const form = document.getElementById("modal-form");
  const type = form.dataset.type;
  const data = Object.fromEntries(new FormData(form));

  let postFunc =
    type === "addClass"
      ? postClass
      : type === "addTask"
      ? postTask
      : type === "addEvent"
      ? postEvent
      : null;

  if (!postFunc) return;

  // Handle linked tasks
  if (type === "addTask" && data.linked_to) {
    const [linkType, linkTitle] = data.linked_to.split("::");
    if (linkType && linkTitle) {
      data.linked_to = { type: linkType, title: linkTitle };
    } else {
      delete data.linked_to;
    }
  }

  // Special handling for classes
  if (type === "addClass") {
    data.online = form.querySelector('[name="online"]').checked;

    // Recurring in-person class
    if (!data.online) {
      data.days = [...form.querySelectorAll('input[name="days"]:checked')].map(
        (d) => d.value
      );
      const term = form.querySelector('input[name="term"]:checked')?.value;
      const year = form.querySelector('select[name="year"]').value;

      if (!term || !year) {
        alert("Term and year are required.");
        return;
      }

      fetch(`/api/term-dates/${term}/${year}`)
        .then((res) => res.json())
        .then(({ start_date, end_date }) => {
          data.start_date = start_date;
          data.end_date = end_date;

          return postRecurringClass(userId, data);
        })
        .then(() => {
          closeModal();
          updateViewRequest(userId, focusedDate);
        })
        .catch((err) => {
          console.error("Error submitting recurring class:", err);
          alert("Failed to submit recurring class: " + err.message);
        });

      return;
    }

    // Online class (skip term/days)
    data.start_time = data.start_time || null;
    data.end_time = data.end_time || null;
  }

  if (type === "addEvent") {
    const isRecurring = form.querySelector("#recurringCheckbox")?.checked;

    if (isRecurring) {
      data.days = [
        ...form.querySelectorAll('input[name="recurring_days"]:checked'),
      ].map((d) => d.value);

      data.start_time = data.start_time || null;
      data.end_time = data.end_time || null;

      return postRecurringEvent(userId, {
        title: data.title,
        location: data.location,
        start_time: data.start_time,
        end_time: data.end_time,
        start_date: data.start_date,
        end_date: data.end_date,
        days: data.days,
      })
        .then(() => {
          closeModal();
          updateViewRequest(userId, focusedDate);
        })
        .catch((err) => {
          console.error("Error submitting recurring event:", err);
          alert("Failed to submit recurring event: " + err.message);
        });
    }

    // One-time event
    data.event_date = data.date;
    delete data.date;
  }

  // Submit tasks, events, or online classes
  postFunc(userId, data)
    .then(() => {
      closeModal();
      updateViewRequest(userId, focusedDate);
    })
    .catch((err) => {
      console.error("Error submitting:", err);
      alert("Failed to submit: " + err.message);
    });
}

export function closeModal() {
  document.getElementById("modal-overlay").classList.add("hidden");
}
