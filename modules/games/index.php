<?php
if ($app->getRequest()->getParam(1) == "sudoku") {
  render_template('pages/games/sudoku.php');
} else {
  render_template('pages/games/games.php');
}
