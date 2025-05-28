document.addEventListener("DOMContentLoaded", () => {
  const loginForm = document.getElementById("login-form");
  const registerForm = document.getElementById("register-form");

  async function handleAuth(endpoint) {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const res = await fetch(`/${endpoint}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    const data = await res.json();

    if (res.ok) {
      localStorage.setItem("user_id", data.user_id);
      alert(data.msg);
      window.location.href = "/index.html";
    } else {
      alert(data.detail || "Authentication failed");
    }
  }

  if (loginForm) {
    loginForm.addEventListener("submit", (e) => {
      e.preventDefault();
      handleAuth("login");
    });
  }

  if (registerForm) {
    registerForm.addEventListener("submit", (e) => {
      e.preventDefault();
      handleAuth("register");
    });
  }
});
