<?php
define('PET_SITE', true);
session_start();
require("core/functions.php");
require("core/App.class.php");

$app = new App();

$app->randomEvent();

$module = $app->getRequest()->getModulePath();
if ($path == '/') {
  require_once($module);
} else if (file_exists($module)) {
  require_once($module);
} else {
  http_response_code(404);
  require_once("./views/error/404.php");
}
