<?php
if ($req->getParam(1) == "thread") {
  $req->renderTemplate('pages/forums/thread.php');
} else if ($req->getParam(1) == "board") {
  $req->renderTemplate('pages/forums/board.php');
} else if ($req->getParamCount() == 1){
  $req->renderTemplate('pages/forums/forums.php');
} else {
  $req->throw404();
}
