<?php
if ($req->subpathEquals("recover")) {
  $req->renderTemplate('pages/login/recover.php');
} else {
  $req->renderTemplate('pages/login/login.php');
}
