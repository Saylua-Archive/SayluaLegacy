<?php
define('PET_SITE', true);
session_start();
require("core/functions.php");
require("core/App.class.php");

$app = new App();

$app->randomEvent();

$module = $app->getRequest()->getModulePath();
if ($path == '/') {
  require($module);
} else if (file_exists($module)) {
  require($module);
} else {
  $app->throw404();
}
