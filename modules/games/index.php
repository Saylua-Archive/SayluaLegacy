<?php
if ($app->getRequest()->getParam(1) == "sudoku") {
  $app->renderTemplate('pages/games/sudoku.php');
} else {
  $app->renderTemplate('pages/games/games.php');
}
