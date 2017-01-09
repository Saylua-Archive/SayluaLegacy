import BaseModel from "./BaseModel";
import Matrix from "./Matrix";

import cloneDeep from "lodash.clonedeep";

const LB_FPS = 60;
const LB_MIN_TIMEOUT = 10;
const LB_PIECES = [[0, 1, 0, 0, // i
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
    this.frames = 0;
    this.lastDrop = 0;
    this.timeout = 300;
    this.gameOver = false;
    this.paused = false;
    this.fast = false;
    this.score = 0;
    this.gameMatrix = new Matrix(18, 10);
    this.placedPieces = new Matrix(18, 10);
    this.nextPiece = null;
    this.piece = {"matrix": new Matrix(4, 4), "r": -3, "c": 2};
  }

  start() {
    this.clearGameState();

    this.getNextPiece();

    setInterval(this.timeStep.bind(this), 1000 / LB_FPS);
  }

  checkGameOver() {
    // If the first row has any pieces, there is a game over.
    let matrix = this.placedPieces;
    for (let i = 0; i < matrix.width; i++) {
      if (matrix.get(0, i)) return true;
    }
    return false;
  }

  timeStep() {
    if (this.paused || this.gameOver) return;

    this.frames++;

    let timeout = this.timeout;
    if (this.fast) {
      timeout = LB_MIN_TIMEOUT;
    }
    if ((this.frames - this.lastDrop) / LB_FPS >= timeout / 1000) {
      this.lastDrop = this.frames;
      this.movePieceDown();
      this.draw();
    }
  }

  movePieceDown() {
    let p = this.piece;
    if (this.validPlacement(p.matrix, p.r + 1, p.c)) {
      p.r++;
      return true;
    }
    // If moving down is invalid, the piece cannot fall anymore.
    this.placedPieces.addMatrix(p.matrix, p.r, p.c);

    if (this.checkGameOver()) {
      // GAME OVER.
      this.piece = null;
      this.gameOver = true;
      
      this.triggerUpdate();
    } else {
      this.getNextPiece();

      // Check if a line was made.
      if (this.clearLines(p.r, p.r + 4).length > 0) {
        this.score += 50;
        this.timeout -= 2;
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
    let i = Math.floor(Math.random() * LB_PIECES.length);
    this.nextPiece = new Matrix(4, 4, LB_PIECES[i]);
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
    this.triggerUpdate();
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