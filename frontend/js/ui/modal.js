import { postClass, postTask, postEvent } from "../utils/api.js";
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
    const classes = JSON.parse(localStorage.getItem("user_classes") || "[]");
    const events = JSON.parse(localStorage.getItem("user_events") || "[]");

    // Deduplicate by title
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

  if (type === "addClass") {
    title.textContent = "Add Class";
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

  if (type === "addEvent") {
    title.textContent = "Add Event";
    form.innerHTML = `...`;
  }
}

export function submitModal(userId, focusedDate, setFocusedDate) {
  const form = document.getElementById("modal-form");
  const type = form.dataset.type;
  const data = Object.fromEntries(new FormData(form)); // raw form data

  console.log("🟡 Form submission started for type:", type);
  console.log("🟡 Raw form data collected:", data);

  if (type === "addTask" && data.linked_to) {
    const [linkType, linkTitle] = data.linked_to.split("::");
    if (linkType && linkTitle) {
      data.linked_to = {
        type: linkType,
        title: linkTitle,
      };
    } else {
      delete data.linked_to;
    }
  }

  const postFunc =
    type === "addClass"
      ? postClass
      : type === "addTask"
      ? postTask
      : type === "addEvent"
      ? postEvent
      : null;

  if (type === "addClass") {
    data.online = form.querySelector('[name="online"]').checked;

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

          console.log(
            "🟡 Final recurring class data before postClass():",
            data
          );
          return postFunc(userId, data); // 👈 passing userId + data separately
        })
        .then(() => {
          closeModal();
          updateViewRequest(userId, focusedDate);
        })
        .catch((err) => {
          console.error("❌ Error submitting class (recurring):", err);
          alert("Failed to submit class: " + err.message);
        });

      return;
    } else {
      console.log("🟡 Posting online class data:", data);
    }
  }

  if (postFunc) {
    console.log("📤 Calling postFunc() with:", { userId, data });

    postFunc(userId, data)
      .then(() => {
        closeModal();
        updateViewRequest(userId, focusedDate);
      })
      .catch((err) => {
        console.error("❌ Error submitting:", err);
        alert("Failed to submit: " + err.message);
      });
  }
}

export function closeModal() {
  document.getElementById("modal-overlay").classList.add("hidden");
}
