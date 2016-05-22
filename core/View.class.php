<?php
class View {
  public $page_title = "";
  public $fullscreen = false;
  public $header_scripts = array();

  private $name;
  private static $view_path = "./views/";

  function __construct($view_name, array $vars = null) {
    $this->name = $view_name;
    if ($vars) {
      # Mapes the vars parameter into the object namespace.
      foreach ($vars as $key => $value) {
        $this->{$key} = $value;
      }
    }
  }

  function render() {
    include($this::$view_path . $this->name);
  }
}
