var delineator = "_";

var gridId = "line-blocks-grid";
var nextId = "line-blocks-next";
var textId = "line-blocks-text";

var width = 10;
var height = 20;

var matrixIdentifier = "line-blocks";
var matrix = new Array(height);

window.addEventListener("load", function () {
  document.getElementById(gridId).innerHTML = createTable(width, height, "matrix", matrixIdentifier);

  document.getElementById(nextId).innerHTML = createNextDisplay();

  window.addEventListener("keydown", function (e) {
    e = e || window.event;
    switch(e.keyCode) {
  		case 37: moveLeft();
  			break;
  		case 38: rotate();
  			break;
  		case 39: moveRight();
  			break;
  		case 40: drop();
  			break;
    }
  });

  init();
  run();
});

function createTable(w, h, tableId, identifier) {
	var table = "<table id='" + tableId + "'>";

	for(var i = 0; i < h; i++){
		table += "<tr id='" + identifier + i + "' >";
		for(var j = 0; j < w; j++) {
			table += "<td id='" + identifier + i + delineator + j + "'></td>";
		}

		table += "</tr>";
	}

	table += "</table>";
	return table;
}

function createNextDisplay() {
	return createTable(4, 4, "displayNext", "next");
}

function init() {
	block = createBlock();
	nextBlock = createBlock();

	for (var i = 0; i < height; i++){
		matrix[i] = new Array(width);
	}

	time = 200;
	score = 0;
	x = width / 2 - 2;
	y = -1;
}



var nextBlock;

var block;

var time = 200;

var score = 0;

var x = width/2 - 2;

var y = -1;

function run() {

	y++;

	if(invalidPosition(block)) {

		//y--;

		addToMatrix();

		block = nextBlock;

		nextBlock = createBlock();

		y = -1;

		x = width / 2 - 2;

	}

	clear();

	draw();

	document.getElementById(textId).innerHTML = "Score:" + score;

	if(gameOver()) {
		document.getElementById(textId).innerHTML += "GAME OVER";
	} else {
		setTimeout("run()", time);
	}
}


function draw() {
	displayNext(nextBlock);

	drawMatrix();
	drawBlock();
}



function rotate() {
	var temp = new Array(4);

	for(var i = 0; i < 4; i++) {
		temp[i] = new Array(4);

		for(var j = 0; j < 4; j++) {
			temp[i][j] = block[3-j][i];
		}
	}

	if(invalidPosition(temp)) return;

	for(var i = 0; i < 4; i++){
		for(var j = 0; j < 4; j++){
			block[i][j] = temp[i][j];
		}
	}
}



function moveLeft() {
	x--;
	if(invalidPosition(block)) {
		x++;
	}
}



function moveRight() {
	x++;
	if(invalidPosition(block)) {
		x--;
	}
}



function drop() {
	while(!invalidPosition(block)) {
		y++;
	}
	y--;
}


function invalidPosition(aBlock) {
	for(var i = 0; i < 4; i++) {
		for(var j = 0; j < 4; j++) {
			var mx = x + j;
			var my = y + i;
			if(aBlock[i][j]) {
				if(mx < 0 || mx >= width || my < -1 || my >= height) {
					return true;
				} else if(matrix[my][mx]) {
					return true;
				}
			}
		}
	}
	return false;
}



function clear() {
	for(var i = height - 1; i >= 0; i--) {
		var clear = true;
		for(var j = 0; j < width; j++) {
			if(!matrix[i][j]) {
				clear = false;
				break;
			}
		}

		if(clear) {
			time--;
			score++;

			if(time < 100) time = 100;

			for(var l = i; l > 0; l--) {
				for(var j = 0; j < width; j++) {
					matrix[l][j] = matrix[l - 1][j];
				}
			}

			for(var j = 0; j < width; j++) {
				matrix[l][j] = 0;
			}

			i++;
		}
	}
}



function addToMatrix() {
	for(var i = 0; i < 4; i++) {
		for(var j = 0; j < 4; j++) {
			if(block[i][j]) {
				matrix[y + i - 1][x + j] = block[i][j];
			}
		}
	}
}



function drawBlock() {
	for (var i = 0; i < 4; i++) {
		for (var j = 0; j < 4; j++) {
			if (block[i][j]) {
				var color = getColor(block[i][j]);
				document.getElementById(matrixIdentifier + (y + i) + delineator + (x + j)).style.backgroundColor = color;
			}
		}
	}
}



function drawMatrix() {
	for(var i = 0; i < height; i++) {
		for(var j = 0; j < width; j++) {
			var color = getColor(matrix[i][j]);
			document.getElementById(matrixIdentifier + i + delineator + j).style.backgroundColor = color;
		}
	}
}



function getColor(value) {
	switch(value) {
		case 1: return "#FFF";
		case 2: return "#0FF";
		case 3: return "#F0F";
		case 4: return "#FF0";
		case 5: return "#0F0";
		case 6: return "#00F";
		case 7: return "#F00";
		default: return "#000";
	}
}


function gameOver() {
	return y == -1 && (invalidPosition(block));
}


function displayNext(block) {
	for(var i = 0; i < 4; i++) {
		for(var j = 0; j < 4; j++) {
			var color = getColor(block[i][j]);
			document.getElementById("next" + i + delineator + j).style.backgroundColor = color;
		}
	}
}



function createBlock() {
	var whichBlock = Math.floor(Math.random() * 7);

	var block = new Array(4);

	block[0] = new Array(4);

	block[1] = new Array(4);

	block[2] = new Array(4);

	block[3] = new Array(4);

	//x, y

	//00	10	20	30

	//01	11	21	31

	//02	12	22	32

	//03	13	23	33

	switch(whichBlock){

		case 0://o

			block[1][1] = 1;

			block[1][2] = 1;

			block[2][1] = 1;

			block[2][2] = 1;

			break;

		case 1://z

			block[1][0] = 2;

			block[1][1] = 2;

			block[2][1] = 2;

			block[2][2] = 2;

			break;

		case 2://s

			block[2][0] = 3;

			block[1][1] = 3;

			block[1][2] = 3;

			block[2][1] = 3;

			break;

		case 3://i

			block[1][0] = 4;

			block[1][1] = 4;

			block[1][2] = 4;

			block[1][3] = 4;

			break;

		case 4://j

			block[1][0] = 5;

			block[2][0] = 5;

			block[1][1] = 5;

			block[1][2] = 5;

			break;

		case 5://l

			block[1][0] = 6;

			block[1][1] = 6;

			block[1][2] = 6;

			block[2][2] = 6;

			break;

		case 6://t

			block[1][0] = 7;

			block[1][1] = 7;

			block[1][2] = 7;

			block[2][1] = 7;

			break;

	}

	return block;

}
