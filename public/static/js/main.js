document.addEventListener("DOMContentLoaded", () => {
  const yearNode = document.getElementById("year");
  if (yearNode) {
    yearNode.textContent = new Date().getFullYear();
  }

  const flashNodes = document.querySelectorAll(".flash");
  flashNodes.forEach((flashNode) => {
    setTimeout(() => {
      flashNode.style.opacity = "0";
      flashNode.style.transform = "translateY(-6px)";
      flashNode.style.transition = "all 0.2s ease";
    }, 4000);
  });
});
