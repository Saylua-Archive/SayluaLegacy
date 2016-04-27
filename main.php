<?php

define('PET_SITE', true);
session_start();
$path = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);

if ($path == '/') {
  require_once('./modules/home/index.php');
} else if (file_exists('./modules'.$path."/index.php")) {
  require_once('./modules'.$path."/index.php");
} else {
  echo "I can't find the file ".'./modules'.$path."/index.php";
}
