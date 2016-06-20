<?php
include ("Request.class.php");
include ("View.class.php");
include ("User.class.php");

class App {
  private $request;
  private $user;

  function __construct() {
    $this->request = new Request();
    $this->user = new User();
  }

  function renderTemplate($name, array $vars = []) {
    $vars['user'] = $this->user;
    $vars['is_logged_in'] = $this->isLoggedIn();

    $view = new View($name, $vars);
    $view->render();
  }

  function throw404() {
    http_response_code(404);
    $this->renderTemplate("error/404.php");
  }

  function randomEvent() {
    if (rand(0, 5) > 4) {
      $_SESSION['random_event']['title'] = "Woah, a thing is happening. ";
      $_SESSION['random_event']['body'] = "You found gum on the bottom of your shoe. ";
    } else if (rand(0, 10) > 7) {
      $_SESSION['random_event']['title'] = "Hahaha, things are happening. ";
      $_SESSION['random_event']['body'] = "A wild raccoon dropped a bunch of gold in front of you. ";
    }
  }

  function getRequest() {
    return $this->request;
  }

  function isLoggedIn() {
    return true;
  }

  function getUser() {
    return $this->user;
  }
}
