<?php

define('PET_SITE', true);
session_start();
$path = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);

$_SERVER['PARAMS'] = preg_split('@/@', $path, NULL, PREG_SPLIT_NO_EMPTY);

include('views/top.php');

if (rand(0, 3) > 2) {
  include('views/random-event.php');
}

$module = './modules/home/index.php';
if (count($_SERVER['PARAMS']) > 0) {
  $module = './modules/' . $_SERVER['PARAMS'][0]. "/index.php";
}

if ($path == '/') {
  require_once($module);
} else if (file_exists($module)) {
  require_once($module);
} else {
  echo "I can't find the file " . $module;
}
include('views/bottom.php');
