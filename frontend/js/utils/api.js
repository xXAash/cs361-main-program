// 📤 Fetch all classes for a user
export async function fetchClasses(userId) {
  const res = await fetch(`/api/classes/${userId}`);
  return res.json();
}

// 📤 Fetch all events for a user
export async function fetchEvents(userId) {
  const res = await fetch(`/api/events/${userId}`);
  return res.json();
}

// 📤 Fetch all tasks for a user
export async function fetchTasks(userId) {
  const res = await fetch(`/api/tasks/${userId}`);
  return res.json();
}

// 🆕 POST a class (expects userId and classData)
export async function postClass(userId, classData) {
  return fetch("/api/classes", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      user_id: userId,
      new_class: classData,
    }),
  }).then((res) => {
    if (!res.ok) {
      return res.text().then((text) => {
        throw new Error(`Failed to post class: ${res.status} ${text}`);
      });
    }
    return res.json();
  });
}

// 🆕 POST a task (expects userId and taskData)
export async function postTask(userId, taskData) {
  console.log("📤 Sending to /api/tasks:", {
    user_id: userId,
    new_task: taskData,
  });
  return fetch("/api/tasks", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      user_id: userId,
      new_task: taskData,
    }),
  }).then((res) => {
    if (!res.ok) {
      return res.text().then((text) => {
        throw new Error(`Failed to post task: ${res.status} ${text}`);
      });
    }
    return res.json();
  });
}

export async function postRecurringClass(userId, classData) {
  return fetch("/api/classes/recurring", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      user_id: userId,
      ...classData,
    }),
  }).then((res) => {
    if (!res.ok) {
      return res.text().then((text) => {
        throw new Error(
          `Failed to post recurring class: ${res.status} ${text}`
        );
      });
    }
    return res.json();
  });
}

export async function postEvent(userId, eventData) {
  return fetch("/api/events", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      user_id: userId,
      new_event: eventData, // already formatted in modal.js
    }),
  }).then((res) => {
    if (!res.ok) {
      return res.text().then((text) => {
        throw new Error(`Failed to post event: ${res.status} ${text}`);
      });
    }
    return res.json();
  });
}

export async function postRecurringEvent(userId, eventData) {
  return fetch("/api/events/recurring", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      user_id: userId,
      ...eventData,
    }),
  }).then((res) => {
    if (!res.ok) {
      return res.text().then((text) => {
        throw new Error(
          `Failed to post recurring event: ${res.status} ${text}`
        );
      });
    }
    return res.json();
  });
}
