import BaseModel from "./BaseModel";
import Matrix from "./Matrix";

import cloneDeep from "lodash.clonedeep";

var pieceData = [[0, 1, 0, 0, // i
                  0, 1, 0, 0,
                  0, 1, 0, 0,
                  0, 1, 0, 0],

                 [0, 0, 2, 0, // j
                  0, 0, 2, 0,
                  0, 2, 2, 0,
                  0, 0, 0, 0],

                 [0, 3, 0, 0, // l
                  0, 3, 0, 0,
                  0, 3, 3, 0,
                  0, 0, 0, 0],

                 [0, 0, 0, 0, // o
                  0, 4, 4, 0,
                  0, 4, 4, 0,
                  0, 0, 0, 0],

                 [0, 0, 0, 0, // t
                  5, 5, 5, 0,
                  0, 5, 0, 0,
                  0, 0, 0, 0],

                 [0, 0, 0, 0, // s
                  0, 6, 6, 0,
                  6, 6, 0, 0,
                  0, 0, 0, 0],

                 [0, 0, 0, 0, // z
                  7, 7, 0, 0,
                  0, 7, 7, 0,
                  0, 0, 0, 0]];

// GameState
// --------------------------------------
// Keeps track of the player's current tetris state.

export default class GameState extends BaseModel {
  constructor() {
    super();
    this.start();
  }

  clearGameState() {
    this.timeout = 300;
    this.gameOver = false;
    this.paused = false;
    this.fast = false;
    this.score = 0;
    this.gameMatrix = new Matrix(18, 10);
    this.placedPieces = new Matrix(18, 10);
    this.nextPiece = null;
    this.piece = {"matrix": new Matrix(4, 4), "r": -1, "c": 2};
  }

  start() {
    this.clearGameState();

    this.getNextPiece();

    setTimeout(this.timeStep.bind(this), this.timeout);
  }

  endGame() {
    this.gameOver = true;
  }

  timeStep() {
    if (this.paused || this.gameOver) return;

    this.movePieceDown();
    this.draw();

    let t = this.timeout;
    if (this.fast) {
      t = 10;
    }

    // HACK. Speedup in timeout. Awful, truly awful. Much hackish
    setTimeout(this.timeStep.bind(this), t);
  }

  movePieceDown() {
    let p = this.piece;
    // Each time the clock ticks, we move the piece down if it's valid.
    if (this.validPlacement(p.matrix, p.r + 1, p.c)) {
      p.r++;
      return true;
    }
    // If moving down is invalid, the piece cannot fall anymore.
    let gameOver = false;
    for (let i = 0; !gameOver && i + p.r < 0; i++) {
      for (let j = 0; !gameOver && j < p.matrix.width; j++) {
        gameOver = !!p.matrix.get(i, j);
      }
    }

    if (gameOver) {
      this.endGame();
    } else {
      this.placedPieces.addMatrix(p.matrix, p.r, p.c);
      this.getNextPiece();

      // Check if a line was made.
      if (this.clearLines(p.r, p.r + 4).length > 0) {
        this.score++;
        this.timeout--;
      }
    }
    return false;
  }

  clearLines(minRow, maxRow) {
    let matrix = this.placedPieces;
    let deleted = [];

    for (let i = minRow; i < maxRow; i++) {
      let j = 0;
      while (matrix.get(i, j) && j < matrix.width) {
        j++;
      }
      if (j == matrix.width) {
        // There is a line at i.
        deleted.push(i);
      }
    }
    matrix.deleteRows(deleted);
    return deleted;
  }

  validPlacement(piece, r, c) {
    let matrix = this.placedPieces;
    for (let i = 0; i < piece.height; i++) {
      for (let j = 0; j < piece.width; j++) {
        let row = r + i;
        let col = c + j;

        if (matrix.withinBounds(row, col)) {
          // If the piece intersects another piece.
          if (piece.get(i, j) && matrix.get(row, col)) {
            return false;
          }
        } else if (row >= 0 && piece.get(i, j)) {
          // If the piece goes past the sides or the bottom.
          // (don't count the top)
          return false;
        }
      }
    }
    return true;
  }

  getNextPiece() {
    if (!this.nextPiece) {
      this.setNextPiece();
    }
    this.piece = {"matrix": this.nextPiece, "r": -2, "c": 3};
    this.setNextPiece();
  }

  setNextPiece() {
    let pieces = pieceData;
    let i = Math.floor(Math.random() * pieces.length);
    this.nextPiece = new Matrix(4, 4, pieces[i]);
  }

  draw() {
    let matrix = cloneDeep(this.placedPieces);
    let p = this.piece;
    matrix.addMatrix(p.matrix, p.r, p.c);

    // gameMatrix is bound to a BlockGrid, which should render this.
    this.gameMatrix = matrix;

    // Make sure the component updates.
    this.triggerUpdate();
  }

  pause() {
    this.paused = !this.paused;
  }

  drop() {
    if (this.paused || this.gameOver) return;
    while (this.movePieceDown());
    this.draw();
  }

  speedUp() {
    this.fast = true;
  }

  speedDown() {
    this.fast = false;
  }

  rotate() {
    if (this.paused || this.gameOver) return;
    let p = cloneDeep(this.piece);
    p.matrix.rotate();
    if (this.validPlacement(p.matrix, p.r, p.c)) {
      this.piece = p;
      this.draw();
    }
  }

  moveLeft() {
    if (this.paused || this.gameOver) return;
    let p = this.piece;
    if (this.validPlacement(p.matrix, p.r, p.c - 1)) {
      p.c--;
      this.draw();
    }
  }

  moveRight() {
    if (this.paused || this.gameOver) return;
    let p = this.piece;
    if (this.validPlacement(p.matrix, p.r, p.c + 1)) {
      p.c++;
      this.draw();
    }
  }
}
