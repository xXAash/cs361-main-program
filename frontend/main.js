let focusedDate = new Date(); // today's date

function formatDate(date) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`; // "YYYY-MM-DD"
}

function formatTime24to12(timeStr) {
  if (!timeStr) return "Unknown time";
  const [hour, minute] = timeStr.split(":").map(Number);
  const ampm = hour >= 12 ? "PM" : "AM";
  const hour12 = hour % 12 === 0 ? 12 : hour % 12;
  return `${hour12}:${minute.toString().padStart(2, "0")} ${ampm}`;
}

function parseEntry(line) {
  const entry = {};
  line.split("|").forEach((segment) => {
    const [key, ...rest] = segment.trim().split(":");
    if (key && rest.length > 0) {
      entry[key.trim()] = rest.join(":").trim();
    }
  });
  return entry;
}

function formatDateLong(dateStr) {
  if (!dateStr) return "Unknown date";

  const [year, month, day] = dateStr.split("-").map(Number);
  const date = new Date(year, month - 1, day);

  const dayNum = date.getDate();
  const suffix =
    dayNum % 10 === 1 && dayNum !== 11
      ? "st"
      : dayNum % 10 === 2 && dayNum !== 12
      ? "nd"
      : dayNum % 10 === 3 && dayNum !== 13
      ? "rd"
      : "th";

  const monthName = date.toLocaleString("default", { month: "long" });

  return `${monthName} ${dayNum}${suffix}, ${year}`;
}

function formatAssignment(entry) {
  return `${entry.title || "Untitled"} for ${
    entry.class || "Unknown class"
  } - Due on ${formatDateLong(
    entry.due_date || entry.due
  )} at ${formatTime24to12(entry.due_time)}`;
}

function formatClassEvent(entry) {
  const title = entry.title || "Untitled";
  const location =
    entry.location && entry.location.trim() !== "" ? entry.location : null;
  const date = formatDateLong(entry.date);
  const start = formatTime24to12(entry.start_time);
  const end = formatTime24to12(entry.end_time);

  if (entry.recurring === "true" && entry.recurring_days) {
    const days = entry.recurring_days
      .split(",")
      .join(", ")
      .replace(/, ([^,]*)$/, ", and $1");

    return location
      ? `${title} at ${location} - ${date} (${days}) from ${start} to ${end}`
      : `${title} - ${date} (${days}) from ${start} to ${end}`;
  } else {
    return location
      ? `${title} at ${location} - ${date} from ${start} to ${end}`
      : `${title} - ${date} from ${start} to ${end}`;
  }
}

function renderDateWheel() {
  const wheel = document.getElementById("date-wheel");
  wheel.innerHTML = "";

  for (let i = 2; i >= -2; i--) {
    const d = new Date(focusedDate);
    d.setDate(d.getDate() + i);

    const div = document.createElement("div");
    div.textContent = d.getDate();

    const isFocused = i === 0;

    div.className =
      "rounded-full flex items-center justify-center font-bold transition-all " +
      (isFocused
        ? "cursor-default w-20 h-20 bg-gray-700 text-white text-xl"
        : "cursor-pointer w-14 h-14 bg-gray-300 text-black hover:bg-gray-400");

    if (!isFocused) {
      div.addEventListener("click", () => {
        focusedDate = d;
        renderDateWheel();
      });
    }

    wheel.appendChild(div);
  }

  updateViewRequest();
}

function openModal(type) {
  const modal = document.getElementById("modal-overlay");
  const form = document.getElementById("modal-form");
  const title = document.getElementById("modal-title");

  modal.classList.remove("hidden");
  form.innerHTML = "";

  if (type === "addClass" || type === "addEvent") {
    title.textContent = type === "addClass" ? "Add Class" : "Add Event";

    form.innerHTML = `
      <label class="block font-medium">Title:</label>
      <input type="text" name="title" class="w-full border p-2 rounded" required>

      <label class="block font-medium">Location:</label>
      <input type="text" name="location" class="w-full border p-2 rounded">

      <label class="block font-medium">Recurring?</label>
      <input type="checkbox" name="recurring_toggle" onchange="toggleRecurring(this)">

      <div id="single-date-section">
        <label class="block font-medium">Date:</label>
        <input type="date" name="date" class="w-full border p-2 rounded">
      </div>

      <div id="recurring-date-section" class="hidden">
        <label class="block font-medium">Start Date:</label>
        <input type="date" name="start_date" class="w-full border p-2 rounded">

        <label class="block font-medium">End Date:</label>
        <input type="date" name="end_date" class="w-full border p-2 rounded">

        <label class="block font-medium mt-2">Recurring Days:</label>
        <div class="flex gap-2 flex-wrap">
          ${["Mon", "Tue", "Wed", "Thu", "Fri"]
            .map(
              (day) =>
                `<label><input type="checkbox" name="recurring_days" value="${day}"> ${day}</label>`
            )
            .join("")}
        </div>
      </div>

      <label class="block font-medium mt-2">Time:</label>
      <div class="flex gap-2">
        <input type="time" name="start_time" class="border p-2 rounded w-1/2" required>
        <input type="time" name="end_time" class="border p-2 rounded w-1/2" required>
      </div>
    `;
  }

  if (type === "addAssignment") {
    title.textContent = "Add Assignment";

    form.innerHTML = `
      <label class="block font-medium">Title:</label>
      <input type="text" name="title" class="w-full border p-2 rounded" required>

      <label class="block font-medium">Class:</label>
      <input type="text" name="class" class="w-full border p-2 rounded" placeholder="CS 361">

      <label class="block font-medium">Due Date:</label>
      <input type="date" name="due_date" class="w-full border p-2 rounded" required>

      <label class="block font-medium">Due Time:</label>
      <input type="time" name="due_time" class="w-full border p-2 rounded" required>
    `;
  }

  form.dataset.type = type;
}

function toggleRecurring(checkbox) {
  const recurringSection = document.getElementById("recurring-date-section");
  const singleDateSection = document.getElementById("single-date-section");

  if (checkbox.checked) {
    recurringSection.classList.remove("hidden");
    singleDateSection.classList.add("hidden");
  } else {
    recurringSection.classList.add("hidden");
    singleDateSection.classList.remove("hidden");
  }
}

function submitModal() {
  const form = document.getElementById("modal-form");
  const type = form.dataset.type;
  const inputs = form.querySelectorAll("input");

  const data = {};
  inputs.forEach((input) => {
    if (input.name === "recurring_days" && input.checked) {
      if (!data["recurring_days"]) data["recurring_days"] = [];
      data["recurring_days"].push(input.value);
    } else if (input.name === "recurring_toggle") {
      data["recurring"] = input.checked ? "true" : "false";
    } else if (input.type !== "checkbox") {
      data[input.name] = input.value.trim();
    }
  });

  let line = `type:${type.replace("add", "").toLowerCase()}`;
  for (const key in data) {
    if (Array.isArray(data[key]) && data[key].length > 0) {
      line += ` | ${key}:${data[key].join(",")}`;
    } else if (data[key]) {
      line += ` | ${key}:${data[key]}`;
    }
  }

  fetch("/submit-entry", {
    method: "POST",
    headers: { "Content-Type": "text/plain" },
    body: line,
  })
    .then(() => {
      const script =
        type === "addAssignment"
          ? "services/assignment_service.py"
          : "services/class_event_service.py";

      return fetch("/run-script", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ script }),
      });
    })
    .then(() => {
      closeModal();
      renderDateWheel();
    });
}

function closeModal() {
  document.getElementById("modal-overlay").classList.add("hidden");
}

function updateViewRequest() {
  const dateString = formatDate(focusedDate);
  const requestLine = `date:${dateString}`;

  fetch("/write-view-request", {
    method: "POST",
    headers: { "Content-Type": "text/plain" },
    body: requestLine,
  })
    .then(() => fetch("/dashboard-output.txt"))
    .then((res) => res.text())
    .then((text) => {
      const assignments = [];
      const schedule = [];

      text.split("\n").forEach((line) => {
        const entry = parseEntry(line);
        if (line.includes("type:assignment")) {
          assignments.push(formatAssignment(entry));
        } else if (line.includes("type:class") || line.includes("type:event")) {
          schedule.push(formatClassEvent(entry));
        }
      });

      document.getElementById("schedule-section").innerHTML = schedule
        .map(
          (s) =>
            `<div class="bg-gray-100 px-3 py-2 rounded shadow-sm">${s}</div>`
        )
        .join("");

      document.getElementById("assignment-section").innerHTML = assignments
        .map(
          (a) =>
            `<div class="bg-gray-100 px-3 py-2 rounded shadow-sm">${a}</div>`
        )
        .join("");
    });

  document.getElementById("current-date").textContent =
    focusedDate.toDateString();
}

renderDateWheel();
