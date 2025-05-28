export async function fetchClasses(userId) {
  const res = await fetch(`/api/classes/${userId}`);
  return res.json();
}

export async function fetchEvents(userId) {
  const res = await fetch(`/api/events/${userId}`);
  return res.json();
}

export async function fetchTasks(userId) {
  const res = await fetch(`/api/tasks/${userId}`);
  return res.json();
}

export async function postClass(data) {
  return fetch("/api/classes", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  }).then((res) => {
    if (!res.ok) {
      return res.text().then((text) => {
        throw new Error(`Failed to post class: ${res.status} ${text}`);
      });
    }
    return res.json();
  });
}

export async function postTask(data) {
  return fetch("/api/tasks", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
}

export async function postEvent(data) {
  const recurring = data.recurring_days
    ? {
        is_recurring: true,
        days: data.recurring_days.split(",").map((d) => d.trim()),
        start_date: data.start_date,
        end_date: data.end_date,
      }
    : null;

  const eventData = {
    user_id: data.user_id,
    title: data.title,
    location: data.location,
    start_time: data.start_time,
    end_time: data.end_time,
    date: data.date || null,
    recurring: recurring,
  };

  return fetch("/api/events", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(eventData),
  });
}
