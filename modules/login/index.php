<?php
if ($req->getParam(1) == "recover") {
  $req->renderTemplate('pages/login/recover.php');
} else {
  $req->renderTemplate('pages/login/login.php');
}
