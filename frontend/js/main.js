import { updateViewRequest } from "./ui/render.js";
import { openModal, submitModal, closeModal } from "./ui/modal.js";

let focusedDate = new Date();
let currentView = "daily"; // can be "daily", "weekly", or "monthly"
const userId = localStorage.getItem("user_id");

if (!userId) window.location.href = "/login.html";

// Logout functionality
document.getElementById("logout-btn")?.addEventListener("click", () => {
  localStorage.removeItem("user_id");
  window.location.href = "/login.html";
});

// Arrow navigation
document.getElementById("prev-day")?.addEventListener("click", () => {
  focusedDate.setDate(focusedDate.getDate() - 1);
  renderView();
});

document.getElementById("next-day")?.addEventListener("click", () => {
  focusedDate.setDate(focusedDate.getDate() + 1);
  renderView();
});

// View toggle buttons (optional future setup)
window.setView = (viewType) => {
  currentView = viewType;
  renderView();
};

// Modal logic
window.openModal = (type) => openModal(type);
window.submitModal = () =>
  submitModal(userId, focusedDate, (newDate) => {
    focusedDate = newDate;
    renderView();
  });
window.closeModal = () => closeModal();

// Render logic
function renderView() {
  document.getElementById("current-date").textContent =
    focusedDate.toDateString();
  updateViewRequest(userId, focusedDate, currentView);
}

// Initial load
renderView();
