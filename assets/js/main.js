const menuToggle = document.querySelector(".menu-toggle");
const siteNav = document.querySelector(".site-nav");

if (menuToggle && siteNav) {
  menuToggle.addEventListener("click", () => {
    siteNav.classList.toggle("open");
  });
}

const projectGrid = document.getElementById("projects-grid");
if (projectGrid) {
  fetch("assets/data/projects.json")
    .then((response) => response.json())
    .then((projects) => {
      projectGrid.innerHTML = projects
        .map(
          (project) => `
            <article class="project-card">
              <h3>${project.title}</h3>
              <p>${project.summary}</p>
              <div class="tags">
                ${project.tags.map((tag) => `<span>${tag}</span>`).join("")}
              </div>
              <a href="${project.link}" target="_blank" rel="noreferrer">Open project</a>
            </article>
          `
        )
        .join("");
    })
    .catch(() => {
      projectGrid.innerHTML =
        "<p>Could not load projects data. Check assets/data/projects.json.</p>";
    });
}

const printCvButton = document.getElementById("print-cv");
if (printCvButton) {
  printCvButton.addEventListener("click", () => {
    window.print();
  });
}
