import { updateViewRequest } from "./render.js";

export function renderDateWheel(userId, focusedDate, setFocusedDate) {
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
        setFocusedDate(d);
        renderDateWheel(userId, d, setFocusedDate);
      });
    }

    wheel.appendChild(div);
  }

  updateViewRequest(userId, focusedDate);
}
