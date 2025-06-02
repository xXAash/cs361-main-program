export function renderDeleteTagForm(form) {
  form.innerHTML = `
    <label class="block mb-2">Item Type:</label>
    <select id="delete-tag-type" class="w-full border rounded p-2 mb-4">
      <option value="">Select type</option>
      <option value="task">Task</option>
      <option value="class">Class</option>
      <option value="event">Event</option>
    </select>

    <label class="block mb-2">Select Item:</label>
    <select id="delete-tag-title" class="w-full border rounded p-2 mb-4">
      <option value="">Select item</option>
    </select>

    <label class="inline-flex items-center mb-4">
      <input type="checkbox" id="delete-tag-all" class="mr-2" checked />
      <span>Apply to all with this title</span>
    </label>

    <div id="delete-tag-date-container" class="mb-4 hidden">
      <label class="block mb-2">Apply to Date:</label>
      <input type="date" id="delete-tag-date" class="w-full border rounded p-2" />
    </div>

    <label class="block mb-2 mt-2">Tag to Delete:</label>
    <select id="delete-tag-tags" class="w-full border rounded p-2 mb-2">
      <option value="">Select tag</option>
    </select>

    <button type="button" id="delete-tag-submit" class="mt-4 bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700">
      Delete
    </button>
  `;

  document
    .getElementById("delete-tag-type")
    .addEventListener("change", updateDeleteTitleDropdown);
  document
    .getElementById("delete-tag-title")
    .addEventListener("change", updateDeleteTagDropdown);
  document
    .getElementById("delete-tag-all")
    .addEventListener("change", toggleDeleteTagDate);
  document
    .getElementById("delete-tag-submit")
    .addEventListener("click", submitDeleteTagForm);

  updateDeleteTitleDropdown();
}

function toggleDeleteTagDate() {
  const applyAll = document.getElementById("delete-tag-all").checked;
  document
    .getElementById("delete-tag-date-container")
    .classList.toggle("hidden", applyAll);
}

function updateDeleteTitleDropdown() {
  const type = document.getElementById("delete-tag-type").value;
  const dropdown = document.getElementById("delete-tag-title");
  dropdown.innerHTML = `<option value="">Select item</option>`;

  const userId = localStorage.getItem("user_id");
  if (!userId || !type) return;

  const endpoint = `/api/${
    type === "class" ? "classes" : type + "s"
  }/${userId}`;
  fetch(endpoint)
    .then((res) => res.json())
    .then((items) => {
      const seenTitles = new Set();
      items.forEach((item) => {
        if (!seenTitles.has(item.title)) {
          seenTitles.add(item.title);
          const opt = document.createElement("option");
          opt.value = item.title;
          opt.textContent = item.title;
          dropdown.appendChild(opt);
        }
      });
    })
    .catch((err) => {
      console.error("Error fetching titles:", err);
      alert(`Could not load ${type}s`);
    });
}

function updateDeleteTagDropdown() {
  const type = document.getElementById("delete-tag-type").value;
  const title = document.getElementById("delete-tag-title").value;
  const userId = localStorage.getItem("user_id");
  const dropdown = document.getElementById("delete-tag-tags");

  if (!type || !title || !userId) return;

  const endpoint = `/api/${
    type === "class" ? "classes" : type + "s"
  }/${userId}`;
  fetch(endpoint)
    .then((res) => res.json())
    .then((items) => {
      const applyAll = document.getElementById("delete-tag-all").checked;
      const date = document.getElementById("delete-tag-date").value;
      const tagSet = new Set();

      items.forEach((item) => {
        const matchesTitle = item.title === title;
        let matchesDate = true;

        if (!applyAll && date) {
          const dateField =
            type === "class"
              ? "class_date"
              : type === "event"
              ? "event_date"
              : "due_date";
          matchesDate = item[dateField] === date;
        }

        if (matchesTitle && matchesDate && Array.isArray(item.tags)) {
          item.tags.forEach((tag) => tagSet.add(tag));
        }
      });

      dropdown.innerHTML = `<option value="">Select tag</option>`;
      [...tagSet].forEach((tag) => {
        const opt = document.createElement("option");
        opt.value = tag;
        opt.textContent = tag;
        dropdown.appendChild(opt);
      });
    })
    .catch((err) => {
      console.error("Error fetching tags:", err);
      alert("Could not load tags.");
    });
}

function submitDeleteTagForm() {
  const itemType = document.getElementById("delete-tag-type").value;
  const selectedTitle = document.getElementById("delete-tag-title").value;
  const selectedTag = document.getElementById("delete-tag-tags").value;
  const applyAll = document.getElementById("delete-tag-all").checked;
  const date = document.getElementById("delete-tag-date").value;
  const email = localStorage.getItem("user_email") || "testuser@example.com";

  if (!itemType || !selectedTitle || !selectedTag || (!applyAll && !date)) {
    alert("Please fill out all required fields.");
    return;
  }

  let requestText = `
email=${email}
type=${itemType}
title=${selectedTitle}
tag=${selectedTag}
apply_all=${applyAll}
`.trim();

  if (!applyAll && date) {
    requestText += `\ndate=${date}`;
  }

  fetch("/write-tag-delete", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ content: requestText }),
  })
    .then((res) => {
      if (!res.ok) throw new Error("Write failed");
      waitForDeleteTagResponse();
    })
    .catch((err) => {
      console.error(err);
      alert("Could not write tag delete request.");
    });
}

function waitForDeleteTagResponse() {
  let attempts = 0;
  const interval = setInterval(() => {
    fetch("/read-tag-delete-response")
      .then((res) => res.text())
      .then((data) => {
        if (data && data.trim()) {
          clearInterval(interval);
          alert(data.trim());
          document.getElementById("modal-overlay").classList.add("hidden");
          fetch("/clear-tag-delete-response", { method: "POST" });
        }
      });

    if (++attempts > 10) {
      clearInterval(interval);
      alert("No response from tag delete microservice.");
    }
  }, 1000);
}
