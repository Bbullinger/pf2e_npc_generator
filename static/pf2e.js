const BASE_URL = "http://localhost:5000/";

// preventDefault does not work inside an async function,
// Second eventlistener needed to prevent auto refresh
if (main.dataset.page === "home") {
  generateCharacter.addEventListener("submit", function (e) {
    e.preventDefault();
  });
  generateCharacter.addEventListener("submit", randomizeNpcForm());
}
