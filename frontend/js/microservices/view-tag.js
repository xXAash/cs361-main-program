// Load all unique tags from user's classes, events, and tasks into all 3 dropdowns
function loadAllTags() {
  const userId = localStorage.getItem("user_id");
  if (!userId) {
    alert("User not logged in.");
    return;
  }

  fetch(`/api/tags/${userId}`)
    .then((res) => res.json())
    .then((tags) => {
      if (!Array.isArray(tags)) tags = [];
      const selects = [
        document.getElementById("tag-filter-1"),
        document.getElementById("tag-filter-2"),
        document.getElementById("tag-filter-3"),
      ];
      selects.forEach((select) => {
        // Clear current options except first placeholder
        select
          .querySelectorAll("option:not(:first-child)")
          .forEach((opt) => opt.remove());

        tags.forEach((tag) => {
          const option = document.createElement("option");
          option.value = tag;
          option.textContent = tag;
          select.appendChild(option);
        });
      });
    })
    .catch((err) => {
      console.error("Error loading tags:", err);
      alert("Could not load tags.");
    });
}

// Called on Search button click
function searchByTags() {
  const userId = localStorage.getItem("user_id");
  if (!userId) {
    alert("User not logged in.");
    return;
  }

  // Collect selected tags, ignoring empty selections
  const tags = [
    document.getElementById("tag-filter-1").value.trim(),
    document.getElementById("tag-filter-2").value.trim(),
    document.getElementById("tag-filter-3").value.trim(),
  ].filter((tag) => tag.length > 0);

  if (tags.length === 0) {
    alert("Please select at least one tag.");
    return;
  }

  fetch(`/api/view-tags/${userId}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ tags }),
  })
    .then((res) => res.json())
    .then((data) => {
      displayResults(data);
    })
    .catch((err) => {
      console.error("Error searching by tags:", err);
      alert("Failed to search by tags.");
    });
}

function pollForResponse(attempts = 0) {
  fetch("/read-tag-view-response")
    .then((res) => res.text())
    .then((data) => {
      if (data && data.trim() && !data.startsWith("Error")) {
        try {
          const parsed = JSON.parse(data);
          displayResults(parsed);
          fetch("/clear-tag-view-response", { method: "POST" }); // cleanup
        } catch {
          if (attempts > 10) {
            alert("Invalid response from tag view service.");
          } else {
            setTimeout(() => pollForResponse(attempts + 1), 500);
          }
        }
      } else {
        if (attempts > 10) {
          alert("No response from tag view service. Try again.");
        } else {
          setTimeout(() => pollForResponse(attempts + 1), 500);
        }
      }
    })
    .catch(() => {
      if (attempts > 10) {
        alert("Error reading response from tag view service.");
      } else {
        setTimeout(() => pollForResponse(attempts + 1), 500);
      }
    });
}

// Display returned classes, events, tasks in the page sections
function displayResults(data) {
  data = data || {};
  data.classes = Array.isArray(data.classes) ? data.classes : [];
  data.events = Array.isArray(data.events) ? data.events : [];
  data.tasks = Array.isArray(data.tasks) ? data.tasks : [];

  const scheduleSection = document.getElementById("schedule-section");
  const assignmentSection = document.getElementById("assignment-section");

  // Clear existing
  scheduleSection.innerHTML = "";
  assignmentSection.innerHTML = "";

  // Show classes and events in schedule
  if (data.classes.length === 0 && data.events.length === 0) {
    scheduleSection.textContent =
      "No classes or events match the selected tags.";
  } else {
    [...data.classes, ...data.events].forEach((item) => {
      const div = document.createElement("div");
      div.className = "p-2 border rounded mb-2";

      div.innerHTML = `<strong>${item.title}</strong><br/>
        ${item.location || ""} <br/>
        Date: ${item.class_date || item.event_date} <br/>
        Time: ${item.start_time || ""} - ${item.end_time || ""} <br/>
        Tags: ${item.tags.join(", ")}`;

      scheduleSection.appendChild(div);
    });
  }

  // Show tasks in assignments section
  if (data.tasks.length === 0) {
    assignmentSection.textContent = "No assignments match the selected tags.";
  } else {
    data.tasks.forEach((task) => {
      const div = document.createElement("div");
      div.className = "p-2 border rounded mb-2";

      div.innerHTML = `<strong>${task.title}</strong><br/>
        Due: ${task.due_date} ${task.due_time} <br/>
        Tags: ${task.tags.join(", ")}`;

      assignmentSection.appendChild(div);
    });
  }
}

// Load tags on page load
window.addEventListener("DOMContentLoaded", loadAllTags);
window.searchByTags = searchByTags;
