import { renderAddTagForm } from "./add-tag.js";
import { renderDeleteTagForm } from "./delete-tag.js";

window.openModal = function (type) {
  const modal = document.getElementById("modal-overlay");
  const title = document.getElementById("modal-title");
  const form = document.getElementById("modal-form");

  modal.classList.remove("hidden");
  form.innerHTML = "";
  form.dataset.type = type;

  if (type === "addTag") {
    title.textContent = "Add Tag to Item";
    renderAddTagForm(form);
  }

  if (type === "deleteTag") {
    title.textContent = "Delete Tag from Item";
    renderDeleteTagForm(form);
  }
};

window.closeModal = function () {
  document.getElementById("modal-overlay").classList.add("hidden");
};
