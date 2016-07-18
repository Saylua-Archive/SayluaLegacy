window.addEventListener("load", init_map);

function init_map() {
  var dungeon = document.getElementById('dungeon');
  dungeon.innerHTML = "";
  getMap();
}

const T_WIDTH = 64;
const T_COUNTX = 10;
const T_COUNTY = 8;
const TILE_LOC = "/static/img/tiles/";
const API_MAP_ENDPOINT = "/api/explore/map/";
const API_MOVE_ENDPOINT = "/api/explore/move/";
const PLAYER_OFFSET = 0;

var map = {
  cols: T_COUNTX,
  rows: T_COUNTY,
  tsize: T_WIDTH,
  tiles: new Array(T_COUNTY * T_COUNTX),
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


function getMap() {
  reqwest({
    url: API_MAP_ENDPOINT,
    method: 'GET',
    type: 'json',
    success: function (resp) {
      var jsonData = resp;
      map.tiles = jsonData.map;
      renderMap(map);
      addPlayer(jsonData.player.x, jsonData.player.y);
    }
  });
}

function renderMap(map) {
  var dungeon = document.getElementById('dungeon');
  dungeon.style.width = (T_WIDTH * T_COUNTX) + "px";
  dungeon.style.height = (T_WIDTH * T_COUNTY) + "px";

  var toAdd = document.createDocumentFragment();
  for (var i = 0; i < T_COUNTY; i++) {
    for (var j = 0; j < T_COUNTX; j++) {
       var newDiv = document.createElement('div');
       newDiv.id = j + "_" + i;
       newDiv.className = 'dungeonTile';
       newDiv.style.width = T_WIDTH + "px";
       newDiv.style.height = T_WIDTH + "px";
       if (map.getTile(j, i) == 2) {
         newDiv.style.backgroundColor = "#FF0000";
       } else if (map.getTile(j, i) > 0) {
         newDiv.style.backgroundColor = "#DEB887";
       }
       newDiv.addEventListener("click", findPath);
       newDiv.dataset.x = j;
       newDiv.dataset.y = i;
       toAdd.appendChild(newDiv);
    }
  }
  dungeon.appendChild(toAdd);
}

function addPlayer(x, y) {
  var dungeon = document.getElementById('dungeon');
  var playerDiv = document.createElement('div');
  player = {
    x: 0,
    y: 0
  };
  playerDiv.id = 'player';
  playerDiv.className = 'dungeonObject';
  playerDiv.style.width = T_WIDTH + "px";
  playerDiv.style.height = T_WIDTH + "px";
  playerDiv.style.backgroundImage = "url('/static/img/SHC.png')";
  playerDiv.style.backgroundSize =  T_WIDTH + "px " + T_WIDTH + "px ";
  dungeon.appendChild(playerDiv);
  movePlayer(x, y);
}

function movePlayer(x, y) {
  var playerDiv = document.getElementById('player');
  var target = map.getTile(player.x + x, player.y + y);
  if (target > 0) {
    reqwest({
      url: API_MOVE_ENDPOINT,
      method: 'POST',
      data: player,
      type: 'json',
      success: function (resp) {
        if (target == 2) {
          // Player has found an exit
          init_map();
        } else {
          player.x += x;
          player.y += y;
          playerDiv.style.left =  (player.x * T_WIDTH) + "px";
          playerDiv.style.top =  (player.y * T_WIDTH - PLAYER_OFFSET) + "px";
        }
      }
    });
  }
}

// Allow player to use arrow keys to move
window.addEventListener("keydown", function(e) {
    if (document.activeElement && document.activeElement != document.body) {
      return;
    }
    // space and arrow keys
    if([37, 38, 39, 40].indexOf(e.keyCode) > -1) {
      e.preventDefault();
    }

    checkKey();
}, false);

function checkKey(e) {
    e = e || window.event;

    if (e.keyCode == '38' || e.keyCode == '87') {
      // up arrow
      movePlayer(0, -1);
    } else if (e.keyCode == '40' || e.keyCode == '83') {
      // down arrow
      movePlayer(0, 1);
    } else if (e.keyCode == '37' || e.keyCode == '65') {
      // left arrow
      movePlayer(-1, 0);
    } else if (e.keyCode == '39' || e.keyCode == '68') {
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

function findPath() {
  if (player.x == this.dataset.x && player.y == this.dataset.y) {
    return;
  }
  var queue = [{x : this.dataset.x, y : this.dataset.y}];
  var checked = [];
  var found = false;
  while (queue.length > 0) {
    var currentLocation = queue.shift();
    checked.push(1 * currentLocation.x + 10 * currentLocation.y);
    if (player.x == currentLocation.x - 1 && player.y == currentLocation.y) {
      movePlayer(1, 0);
      return;
    } else if (player.x == 1 * currentLocation.x + 1 && player.y == currentLocation.y) {
      movePlayer(-1, 0);
      return;
    } else if (player.x == 1 * currentLocation.x && player.y == currentLocation.y - 1) {
      movePlayer(0, 1);
      return;
    } else if (player.x == 1 * currentLocation.x && player.y == 1 * currentLocation.y + 1) {
      movePlayer(0, -1);
      return;
    }
    if ((map.getTile(1 * currentLocation.x - 1, 1 * currentLocation.y) != 0) && checked.indexOf(1 * currentLocation.x - 1 + 10 * currentLocation.y) == -1) {
        queue.push({x : 1 * currentLocation.x - 1, y : 1 * currentLocation.y});
    }
    if ((map.getTile(1 * currentLocation.x + 1, 1 * currentLocation.y) != 0) && checked.indexOf(1 * currentLocation.x + 1 + 10 * currentLocation.y) == -1) {
        queue.push({x : 1 * currentLocation.x + 1, y : 1 * currentLocation.y});
    }
    if ((map.getTile(1 * currentLocation.x, 1 * currentLocation.y - 1) != 0) && checked.indexOf(1 * currentLocation.x + 10 * (1 * currentLocation.y - 1)) == -1) {
        queue.push({x : 1 * currentLocation.x, y : 1 * currentLocation.y - 1});
    }
    if ((map.getTile(1 * currentLocation.x, 1 * currentLocation.y + 1) != 0) && checked.indexOf(1 * currentLocation.x + 10 * (1 * currentLocation.y + 1)) == -1) {
        queue.push({x : 1 * currentLocation.x, y : 1 * currentLocation.y + 1});
    }
  }
}
