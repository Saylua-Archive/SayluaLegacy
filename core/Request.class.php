<?php
class Request {
  private $path;
  private $params;
  private static $default_module = './modules/home/index.php';

  function __construct() {
    $this->path = $_SERVER['REQUEST_URI'];
    $this->params = preg_split('@/@', $this->path, NULL,
      PREG_SPLIT_NO_EMPTY);
  }

  function getModulePath() {
    if (count($this->params) > 0) {
      return './modules/' . $this->params[0]. "/index.php";
    }
    return $this::$default_module;
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
}
