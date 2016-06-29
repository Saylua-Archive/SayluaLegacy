<?php
include ("View.class.php");
include ("User.class.php");

class Request {
  private static $default_module = './modules/home/index.php';

  private $path;
  private $subpath;

  private $params;
  private $user = NULL;

  function __construct() {
    $this->path = $_SERVER['REQUEST_URI'];
    if ($this->path) {
      $this->subpath = preg_replace("/\?.*/", "", $this->path);
      $this->subpath = preg_replace("/(^\/+|\/+$)/",
        "", $this->subpath);
      $this->subpath = explode('/', $this->subpath, 2);
      if (count($this->subpath) > 1) {
        $this->subpath = $this->subpath[1];
      } else {
        $this->subpath = "";
      }
    }
    $this->params = preg_split('@[/?]@', $this->path, NULL,
      PREG_SPLIT_NO_EMPTY);

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

  function getModulePath() {
    if (count($this->params) == 2 && $this->params[0] == "api") {
      return './api/' . $this->params[1] . '.php';
    } else if (count($this->params) > 0) {
      return './modules/' . $this->params[0] . '/index.php';
    }
    return $this::$default_module;
  }

  function subpathMatches($regex) {
    return preg_match($regex, $this->subpath);
  }

  function getParamCount() {
    return count($this->params);
  }

  function getParam($number) {
    if ($number >= $this->getParamCount()) {
      return "";
    }
    return $this->params[$number];
  }

  function isLoggedIn() {
    return $this->user != NULL;
  }

  function getUser() {
    return $this->user;
  }
}
