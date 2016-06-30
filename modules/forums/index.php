<?php
if ($req->subpathMatches("/thread\/[0-9]+/")) {
  $req->renderTemplate('pages/forums/thread.php');
} else if ($req->subpathMatches("/board\/[0-9]+/")) {
  $req->renderTemplate('pages/forums/board.php');
} else if ($req->subpathEquals("")){
  $req->renderTemplate('pages/forums/forums.php');
} else {
  $req->throw404();
}
