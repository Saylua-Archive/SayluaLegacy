<?php

$toReturn = array();
$player = array();

$map = array(
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0
);

function fillMap($oldmap) {
  $current = rand(0, 80);
  for ($i=0; $i < 80; $i++) {
    if (rand(0, 3) > 0) {
      $oldmap[$i] = 1;
    }
  }
  return $oldmap;
}





$map = fillMap($map);

$player[x] = -1;
$player[y] = -1;
while($player[x] == -1) {
  $i = rand(0, 80);
  if ($map[$i] === 1) {
    $player[x] = $i % 10;
    $player[y] = floor($i / 10);
  }
}




$toReturn[player] = $player;
$toReturn[map] = $map;

echo json_encode($toReturn);
