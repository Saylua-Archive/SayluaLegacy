<?php
if ($req->getParam(1) == "sudoku") {
  $req->renderTemplate('pages/games/sudoku.php');
} else {
  $req->renderTemplate('pages/games/games.php');
}
