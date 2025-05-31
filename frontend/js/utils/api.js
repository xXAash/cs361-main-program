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

// 🆕 POST an event (expects userId and eventData)
export async function postEvent(userId, eventData) {
  const recurring = eventData.recurring_days
    ? {
        is_recurring: true,
        days: eventData.recurring_days.split(",").map((d) => d.trim()),
        start_date: eventData.start_date,
        end_date: eventData.end_date,
      }
    : null;

  return fetch("/api/events", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      user_id: userId,
      new_event: {
        title: eventData.title,
        location: eventData.location,
        start_time: eventData.start_time,
        end_time: eventData.end_time,
        event_date: eventData.date || null,
        recurring: recurring,
      },
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
