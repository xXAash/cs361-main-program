window.openModal = function (type) {
  const modal = document.getElementById("modal-overlay");
  const title = document.getElementById("modal-title");
  const form = document.getElementById("modal-form");

  modal.classList.remove("hidden");
  form.innerHTML = "";
  form.dataset.type = type;

  if (type === "addTag") {
    title.textContent = "Add Tag to Item";

    form.innerHTML = `
      <label class="block mb-2">Item Type:</label>
      <select id="add-tag-type" class="w-full border rounded p-2 mb-4" onchange="updateTitleDropdown()">
        <option value="">Select type</option>
        <option value="task">Task</option>
        <option value="class">Class</option>
        <option value="event">Event</option>
      </select>

      <label class="block mb-2">Select Item:</label>
      <select id="add-tag-title" class="w-full border rounded p-2 mb-4">
        <option value="">Select item</option>
      </select>

      <label class="inline-flex items-center mb-4">
        <input type="checkbox" id="add-tag-all" class="mr-2" checked onchange="toggleTagDate()" />
        <span>Apply to all with this title</span>
      </label>

      <div id="tag-date-container" class="mb-4 hidden">
        <label class="block mb-2">Apply to Date:</label>
        <input type="date" id="add-tag-date" class="w-full border rounded p-2" />
      </div>

      <label class="block mb-2 mt-2">Tags (comma-separated):</label>
      <input type="text" id="add-tag-tags" class="w-full border rounded p-2 mb-2" placeholder="e.g. cs361,urgent" />
    `;

    // Immediately populate dropdown if type already selected
    updateTitleDropdown();
  }
};

window.toggleTagDate = function () {
  const applyAll = document.getElementById("add-tag-all").checked;
  document
    .getElementById("tag-date-container")
    .classList.toggle("hidden", applyAll);
};

window.updateTitleDropdown = function () {
  const type = document.getElementById("add-tag-type").value;
  const dropdown = document.getElementById("add-tag-title");
  dropdown.innerHTML = `<option value="">Select item</option>`;

  const userId = localStorage.getItem("user_id"); // or however you store it

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
          const option = document.createElement("option");
          option.value = item.title;
          option.textContent = item.title;
          dropdown.appendChild(option);
        }
      });
    })
    .catch((err) => {
      console.error("Error fetching data:", err);
      alert(`Could not load ${type}s`);
    });
};

window.submitModal = function () {
  const type = document.getElementById("modal-form").dataset.type;

  if (type === "addTag") {
    const itemType = document.getElementById("add-tag-type").value;
    const selectedTitle = document.getElementById("add-tag-title").value;
    const tags = document.getElementById("add-tag-tags").value.trim();
    const applyAll = document.getElementById("add-tag-all").checked;
    const date = document.getElementById("add-tag-date").value;
    const email = localStorage.getItem("user_email") || "testuser@example.com";

    // Validation
    if (!itemType || !selectedTitle || !tags || (!applyAll && !date)) {
      alert("Please fill out all required fields.");
      return;
    }

    // Construct the request
    let requestText = `
email=${email}
type=${itemType}
title=${selectedTitle}
tags=${tags}
apply_all=${applyAll}
`.trim();

    if (!applyAll && date) {
      requestText += `\ndate=${date}`;
    }

    fetch("/write-tag-add", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ content: requestText }),
    })
      .then((res) => {
        if (!res.ok) throw new Error("Write failed");
        waitForAddTagResponse();
      })
      .catch((err) => {
        console.error(err);
        alert("Could not write tag request.");
      });
  }
};

function waitForAddTagResponse() {
  let attempts = 0;
  const interval = setInterval(() => {
    fetch("/read-tag-add-response")
      .then((res) => res.text())
      .then((data) => {
        if (data && data.trim()) {
          clearInterval(interval);
          alert(data.trim());
          closeModal();
          fetch("/clear-tag-add-response", { method: "POST" }); // optional cleanup
        }
      });

    if (++attempts > 10) {
      clearInterval(interval);
      alert("No response from tag microservice. Please try again.");
    }
  }, 1000); // check every 1 second (10s total timeout)
}

window.closeModal = function () {
  document.getElementById("modal-overlay").classList.add("hidden");
};
