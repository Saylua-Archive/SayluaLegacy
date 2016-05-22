<?php
include ("Request.class.php");
include ("View.class.php");

class App {
  var $request;
  var $user;

  function __construct() {
    $this->request = new Request();
  }

  function renderTemplate($name, array $vars = null) {
    $view = new View($name, $vars);
    $view->render();
  }

  function throw404() {
    http_response_code(404);
    include("./views/error/404.php");
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
}
