<?php
define('PET_SITE', true);
session_start();
require_once("core/functions.php");

$path = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);

$_SERVER['PARAMS'] = preg_split('@/@', $path, NULL, PREG_SPLIT_NO_EMPTY);

$module = './modules/home/index.php';
if (count($_SERVER['PARAMS']) > 0) {
  $module = './modules/' . $_SERVER['PARAMS'][0]. "/index.php";
}

if (rand(0, 5) > 4) {
  $_SESSION['random_event']['title'] = "Woah, a thing is happening. ";
  $_SESSION['random_event']['body'] = "You found gum on the bottom of your shoe. ";
} else if (rand(0, 10) > 7) {
  $_SESSION['random_event']['title'] = "Hahaha, things are happening. ";
  $_SESSION['random_event']['body'] = "A wild raccoon dropped a bunch of gold in front of you. ";
}

if ($path == '/') {
  require_once($module);
} else if (file_exists($module)) {
  require_once($module);
} else {
  http_response_code(404);
  require_once("./views/error/404.php");
}
