document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".heart").forEach(btn => {
    btn.addEventListener("click", async () => {
      const id = btn.dataset.product;
      const response = await fetch(`/wishlist/toggle/${id}`, {method:"POST"});
      const data = await response.json();
      if (data.login) {
        window.location.href = "/";
        return;
      }
      if (data.ok) {
        btn.classList.toggle("active", data.active);
        btn.textContent = data.active ? "♥" : "♡";
      }
    });
  });

  document.querySelectorAll("form").forEach(form => {
    form.addEventListener("submit", () => {
      const btn = form.querySelector("button[type='submit']");
      if (btn && btn.dataset.lock !== "true") {
        setTimeout(() => {
          btn.disabled = true;
          btn.dataset.lock = "true";
        }, 0);
      }
    });
  });

  setTimeout(() => {
    document.querySelectorAll(".flash").forEach(x => {
      x.style.opacity = "0";
      x.style.transition = "opacity .4s";
      setTimeout(() => x.remove(), 400);
    });
  }, 3000);
});
