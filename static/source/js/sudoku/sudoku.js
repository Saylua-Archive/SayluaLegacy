function readBoard () {
	var puzzle = [];
	for (var i = 0; i < 9; i++) {
		puzzle[i] = [];
		for (var j = 0; j < 9; j++) {
			puzzle[i][j] = document.getElementById((i + 1) + "-" + (j + 1)).value * 1;
		}
	}

	return new Sudoku(puzzle);
}

function Sudoku (p) {
	var self = this;
	var puzzle = p;

	function isValid (num, row, col) {
		// Check if the row is valid
		for (var i = 0; i < puzzle[row].length; i++) {
			if (num === puzzle[row][i]) {
				return false;
			}
		}

		// Check if the column is valid
		for (var i = 0; i < puzzle.length; i++) {
			if (num === puzzle[i][col]) {
				return false;
			}
		}

		// Check if the box is valid
		var rowStart = Math.floor(row / 3) * 3;
		var colStart = Math.floor(col / 3) * 3;
		for (var i = rowStart; i < (rowStart + 3); i++) {
			for (var j = colStart; j < (colStart + 3); j++) {
				if (num === puzzle[i][j]) {
					return false;
				}
			}
		}

		return true;
	}

	function isEmpty (num) {
		num *= 1;
		return num == 0 || num == null || num == NaN || num == false || num == undefined;
	}
}
