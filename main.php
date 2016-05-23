<?php
define('PET_SITE', true);
error_reporting(E_ALL);
session_start();
require("core/functions.php");
require("core/App.class.php");

$app = new App();

$app->randomEvent();

# Loads the proper PHP script based on the current URL
$module = $app->getRequest()->getModulePath();
if (file_exists($module)) {
  require($module);
} else {
  $this->throw404();
}
