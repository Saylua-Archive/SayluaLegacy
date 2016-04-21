window.onload = init;

function init() {
  fillMap(map);
  addPlayer();
}

const T_WIDTH = 64;
const T_COUNT = 8;
const TILE_LOC = "static/img/tiles/"
const PLAYER_OFFSET = 20;

var map = {
  cols: T_COUNT,
  rows: T_COUNT,
  tsize: T_WIDTH,
  tiles: [
    1, 1, 0, 0, 0, 1, 1, 1,
    1, 1, 1, 1, 1, 0, 0, 1,
    0, 1, 1, 0, 1, 0, 1, 1,
    1, 0, 1, 0, 1, 1, 1, 0,
    0, 0, 1, 1, 0, 1, 1, 1,
    0, 1, 1, 1, 1, 1, 1, 0,
    1, 1, 1, 0, 0, 1, 1, 0,
    0, 1, 0, 0, 0, 0, 0, 0
  ],
  getTile: function(col, row) {
    if (col > map.cols - 1 || row > map.rows - 1 || row < 0 || col < 0) {
      return 0;
    }
    return this.tiles[row * map.cols + col];
  }
};

var player = {
  x: 0,
  y: 0
};


function getMask(x, y) {
  var total = 0;
  var north =  2 * (map.getTile(x, y - 1) || 0);
  var west = 8 * (map.getTile(x - 1, y) || 0);
  var east = 16 * (map.getTile(x + 1, y) || 0);
  var south = 64 * (map.getTile(x, y + 1) || 0);
  total += north + west + east + south;
  if (north > 0 && west > 0) {
    total += (map.getTile(x - 1, y - 1) || 0);
  }
  if (north > 0 && east > 0) {
    total += 4 * (map.getTile(x + 1, y - 1) || 0);
  }
  if (south > 0 && west > 0) {
    total += 32 * (map.getTile(x - 1, y + 1) || 0);
  }
  if (south > 0 && east > 0) {
    total += 128 * (map.getTile(x + 1, y + 1) || 0);
  }
  var converter = { "2" : 1, "8" : 2, "10" : 3, "11" : 4, "16" : 5, "18" : 6, "22" : 7, "24" : 8, "26" : 9, "27" : 10, "30" : 11, "31" : 12, "64" : 13, "66" : 14, "72" : 15, "74" : 16, "75" : 17, "80" : 18, "82" : 19, "86" : 20, "88" : 21, "90" : 22, "91" : 23, "94" : 24, "95" : 25, "104" : 26, "106" : 27, "107" : 28, "120" : 29, "122" : 30, "123" : 31, "126" : 32, "127" : 33, "208" : 34, "210" : 35, "214" : 36, "216" : 37, "218" : 38, "219" : 39, "222" : 40, "223" : 41, "248" : 42, "250" : 43, "251" : 44, "254" : 45, "255" : 46, "0" : 47 };
  return converter[total + ""];
}

function fillMap(map) {
  dungeon = document.getElementById('dungeon');
  dungeon.style.width = (T_WIDTH * T_COUNT) + "px";
  dungeon.style.height = (T_WIDTH * T_COUNT) + "px";

  var toAdd = document.createDocumentFragment();
  for (var i = 0; i < T_COUNT; i++) {
    for (var j = 0; j < T_COUNT; j++) {
       var newDiv = document.createElement('div');
       newDiv.id = j + "_" + i;
       newDiv.className = 'dungeonTile';
       newDiv.style.width = T_WIDTH + "px";
       newDiv.style.height = T_WIDTH + "px";
       if (map.getTile(j, i) > 0) {
         newDiv.style.backgroundImage = "url('static/img/tiles/" + getMask(j, i) + ".png')";
       }
       newDiv.addEventListener("click", moveHere);
       newDiv.dataset.x = j;
       newDiv.dataset.y = i;
       toAdd.appendChild(newDiv);
    }
  }
  dungeon.appendChild(toAdd);
}

function addPlayer() {
  dungeon = document.getElementById('dungeon');
  var playerDiv = document.createElement('div');
  playerDiv.id = 'player';
  playerDiv.className = 'dungeonObject';
  playerDiv.style.width = T_WIDTH + "px";
  playerDiv.style.height = T_WIDTH + "px";
  playerDiv.style.backgroundImage = "url('static/img/SHC.png')";
  playerDiv.style.backgroundSize =  T_WIDTH + "px " + T_WIDTH + "px ";
  dungeon.appendChild(playerDiv);
}

function movePlayer(x, y) {
  var playerDiv = document.getElementById('player');
  if (map.getTile(player.x + x, player.y + y) == 1) {
    player.x += x;
    player.y += y;
    playerDiv.style.left =  (player.x * T_WIDTH) + "px";
    playerDiv.style.top =  (player.y * T_WIDTH - PLAYER_OFFSET) + "px";
  }
}

document.onkeydown = checkKey;

window.addEventListener("keydown", function(e) {
    // space and arrow keys
    if([32, 37, 38, 39, 40].indexOf(e.keyCode) > -1) {
        e.preventDefault();
    }
}, false);

function checkKey(e) {

    e = e || window.event;

    if (e.keyCode == '38' || e.keyCode == '87') {
        // up arrow
        movePlayer(0, -1);
    }
    else if (e.keyCode == '40' || e.keyCode == '83') {
        // down arrow
        movePlayer(0, 1);
    }
    else if (e.keyCode == '37' || e.keyCode == '65') {
       // left arrow
       movePlayer(-1, 0);
    }
    else if (e.keyCode == '39' || e.keyCode == '68') {
       // right arrow
       movePlayer(1, 0);
    }
}

function moveHere () {
  if (Math.abs(this.dataset.x - player.x) >  Math.abs(this.dataset.y - player.y)) {
    if (this.dataset.x - player.x > 0) {
      movePlayer(1, 0);
    } else {
      movePlayer(-1, 0);
    }
  } else {
    if (this.dataset.y - player.y > 0) {
      movePlayer(0, 1);
    } else {
      movePlayer(0, -1);
    }
  }
}
