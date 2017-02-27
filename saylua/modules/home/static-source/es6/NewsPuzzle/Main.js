window.addEventListener("load", function () {
  let submit = document.getElementById("puzzle-submit");
  let puzzle = document.getElementById("puzzle-container");

  // A bunch of little utility functions we'll use in the code.
  let getValue = (c) => (c.value || c.innerHTML);
  let isValid = (num) => (num * 1 >= 1 && num * 1 <= 9);

  submit.addEventListener("click", function () {
    // Note this is 2D data (9x9) that is flattened into a 1D array (1x81)
    let numbers = puzzle.getElementsByClassName("puzzle-number");
    let emptyCount = 0;
    let invalidCount = 0;

    let rowCollisions = {},
      colCollisions = {},
      boxCollisions = {};
    for (let i = 0; i < 9; i++) {
      // I wish I could avoid having to make so manny variables. :/
      let rowSet = {},
        colSet = {},
        boxSet = {};
      for (let j = 0; j < 9; j++) {
        // Check rows
        let rCell = numbers[i * 9 + j];
        let rNum = getValue(rCell);
        if (isValid(rNum)) {
          if (rowSet[rNum]) {
            rowCollisions[i] = true;
          }
          rowSet[rNum] = true;
        } else {
          // Note that we only do this for the first check.
          if (rNum == "") {
            emptyCount++;
          } else {
            invalidCount++;
          }
        }

        // Clear any error classes attached to cells before rendering.
        rCell.parentElement.className = "";

        // Check columns.
        let cNum = getValue(numbers[i + j * 9]);
        if (isValid(cNum)) {
          if (colSet[cNum]) {
            colCollisions[i] = true;
          }
          colSet[cNum] = true;
        }

        // Check 3x3 boxes. The indexing here is a little complicated.
        // i represents the index of the "box" (3x3 subsection) we're on (From left to right).
        // j represents the index we're looking at within the i'th box.

        // This calculates the index of the top left corner of the "box".
        let leftCorner = Math.floor(i / 3) * 3 * 9 + (i % 3) * 3;

        // This calculates the number offset from leftCorner.
        let offset = Math.floor(j / 3) * 9 + j % 3;

        let bNum = getValue(numbers[leftCorner + offset]);
        if (isValid(bNum)) {
          if (boxSet[bNum]) {
            boxCollisions[i] = true;
          }
          boxSet[bNum] = true;
        }
      }
    }

    // Do another set of loops to highlight the UI for any errors.
    for (let i = 0; i < 9; i++) {
      for (let j = 0; j < 9; j++) {
        let rowIndex = i + "",
          colIndex = j + "",
          boxIndex = (Math.floor(i / 3) * 3 + Math.floor(j / 3)) + "";
        let errorCount = ((rowIndex in rowCollisions) + (colIndex in colCollisions)
          + (boxIndex in boxCollisions));
        if (errorCount) {
          numbers[i * 9 + j].parentElement.className = "puzzle-error-" + errorCount;
        }
      }
    }
  });
});
