<?php
define('PET_SITE', true);
error_reporting(E_ALL);
session_start();
require("core/functions.php");
require("core/Request.class.php");

$req = new Request();

# Loads the proper PHP script based on the current URL
$module = $req->getModulePath();
if (file_exists($module)) {
  require($module);
} else {
  $req->throw404();
}
