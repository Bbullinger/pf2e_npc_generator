// preventDefault does not work inside an async function,
// Second eventlistener needed to prevent auto refresh
if (main.dataset.page === "home") {
  generateCharacter.addEventListener("click", function (e) {
    e.preventDefault();
  });
  generateCharacter.addEventListener("click", randomizeNpcForm);
}

if (main.dataset.loggedin === "true") {
  displayGroups();
}
