document.addEventListener("DOMContentLoaded", () => {

  const apps = document.querySelectorAll("#nav-sidebar .app");

  apps.forEach(app => {
    app.addEventListener("click", e => {
      e.preventDefault();

      const appName = app.querySelector(".section").innerText.trim();
      const models = app.querySelectorAll("tbody tr");

      const panelTitle = document.getElementById("panel-title");
      const modelCards = document.getElementById("model-cards");

      panelTitle.innerText = appName;
      modelCards.innerHTML = "";

      models.forEach(row => {
        const link = row.querySelector("th a");
        if (!link) return;

        modelCards.innerHTML += `
          <a href="${link.href}" class="model-card">
            <i class="fas fa-table"></i>
            <div>${link.innerText}</div>
          </a>
        `;
      });
    });
  });

});
