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

function getx($n) {
  return $n % 10;
}

function gety($n) {
  return floor($n / 10);
}

function getn($x, $y) {
  return $x + $y * 10;
}

function getValid($oldmap) {
  $current = rand(0, 79);
  while ($oldmap[$current] == 0) {
    $current = rand(0, 79);
  }
  return $current;
}

function floodErase($n) {
  global $oldmap;
  if ($oldmap[$n] == 0) {
    return;
  }
  $oldmap[$n] = 0;
  if (getx($n) > 0) {
    floodErase($n - 1);
  }
  if (gety($n) > 0) {
    floodErase($n - 10);
  }
  if (getx($n) < 9) {
    floodErase($n + 1);
  }
  if (gety($n) < 7) {
    floodErase($n + 10);
  }
}


$map = fillMap($map);
$oldmap = $map;
$current = rand(0, 79);
while ($oldmap[$current] == 0) {
  $current = rand(0, 79);
}
floodErase($current);
for ($i=0; $i < 80; $i++) {
  $map[$i] = $map[$i] - $oldmap[$i];
}






$player[x] = -1;
$player[y] = -1;
while($player[x] == -1) {
  $i = rand(0, 79);
  if ($map[$i] === 1) {
    $player[x] = $i % 10;
    $player[y] = floor($i / 10);
  }
}




$toReturn[player] = $player;
$toReturn[map] = $map;

echo json_encode($toReturn);
