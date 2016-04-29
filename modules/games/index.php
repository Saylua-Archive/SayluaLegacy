<?php
if ($_SERVER['PARAMS'][1] == "sudoku") {
  render_template('pages/games/sudoku.php');
} else {
  render_template('pages/games/games.php');
}
