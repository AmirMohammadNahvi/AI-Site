function applyTheme(theme) {
  const root = document.documentElement;
  const preferred =
    theme === "system"
      ? window.matchMedia("(prefers-color-scheme: dark)").matches
        ? "dark"
        : "light"
      : theme;
  root.classList.toggle("dark", preferred === "dark");
}

document.addEventListener("DOMContentLoaded", () => {
  const theme = document.documentElement.dataset.theme || "system";
  applyTheme(theme);
});
