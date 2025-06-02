export function formatDate(date) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

export function formatTime24to12(timeStr) {
  if (!timeStr) return "Unknown time";
  const [hour, minute] = timeStr.split(":").map(Number);
  const ampm = hour >= 12 ? "PM" : "AM";
  const hour12 = hour % 12 === 0 ? 12 : hour % 12;
  return `${hour12}:${minute.toString().padStart(2, "0")} ${ampm}`;
}

export function formatDateLong(dateStr) {
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

export function formatTask(task) {
  return `${task.title} - Due on ${formatDateLong(
    task.due_date
  )} at ${formatTime24to12(task.due_time)}`;
}

export function formatClassEvent(entry) {
  const title = entry.title || "Untitled";
  const location = entry.location ? ` at ${entry.location}` : "";
  const start = formatTime24to12(entry.start_time);
  const end = formatTime24to12(entry.end_time);

  const rawDate = entry.class_date || entry.event_date;

  if (rawDate) {
    const date = formatDateLong(rawDate);
    return `${title}${location} - ${date} from ${start} to ${end}`;
  } else if (entry.recurring && entry.recurring.is_recurring) {
    const days = entry.recurring.days?.join(", ") || "Unknown days";
    return `${title}${location} - Recurs on ${days} from ${start} to ${end}`;
  } else {
    return title;
  }
}
