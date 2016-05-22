<?php
if ($app->getRequest()->getParam(1) == "thread") {
  render_template('pages/forums/thread.php');
} else if ($app->getRequest()->getParam(1) == "board") {
  render_template('pages/forums/board.php');
} else if ($app->getRequest()->getParamCount() == 1){
  render_template('pages/forums/forums.php');
} else {
  $app->throw404();
}
