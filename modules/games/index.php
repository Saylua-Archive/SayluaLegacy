<?php
if ($req->subpathEquals("sudoku")) {
  $req->renderTemplate('pages/games/sudoku.php');
} else {
  $req->renderTemplate('pages/games/games.php');
}
