window.onload = function () {
  var loginModal = new Modal({
    title: "Login to LyreFly",
    content: document.getElementById("login_menu"),
    linkSelector: ".trigger-login"
  });

  var registerModal = new Modal({
    title: "Register an Account on LyreFly",
    content: document.getElementById("register_menu"),
    linkSelector: ".trigger-register"
  });
}
