<?php
if ($app->getRequest()->getParam(1) == "thread") {
  $app->renderTemplate('pages/forums/thread.php');
} else if ($app->getRequest()->getParam(1) == "board") {
  $app->renderTemplate('pages/forums/board.php');
} else if ($app->getRequest()->getParamCount() == 1){
  $app->renderTemplate('pages/forums/forums.php');
} else {
  $app->throw404();
}
