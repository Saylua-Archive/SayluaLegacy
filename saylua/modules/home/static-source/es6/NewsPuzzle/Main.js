window.addEventListener("load", function () {
  let submit = document.getElementById("puzzle-submit");
  let puzzle = document.getElementById("puzzle-container");

  let getNum = (c) => (c.value || c.innerHTML) * 1;
  let addErrorClass = function (className) {
    if (className.indexOf("puzzle-error-") < 0) {
      return className + " puzzle-error-1";
    }
    return className.replace(/puzzle\-error\-(\d+)/, (match, n) => {
      return "puzzle-error-" + (Number(n) + 1);
    });
  };

  submit.addEventListener("click", function () {
    // Note this is 2D data (9x9) that is flattened into a 1D array (1x81).
    let numbers = puzzle.getElementsByClassName("puzzle-number");
    let emptyCount = 0;
    let invalidCount = 0;
    for (let i = 0; i < 9; i++) {
      let rowSet = {},
        colSet = {},
        boxSet = {};

      let rowHasColllision = false,
        colHasColllision = false,
        boxHasColllision = false;
      for (let j = 0; j < 9; j++) {
        // Check rows
        let rCell = numbers[i * 9 + j];
        let rNum = getNum(rCell);
        rowHasColllision = rowHasColllision || rowSet[rNum];
        rowSet[rNum] = true;

        // Update counts and such.
        rCell.parentElement.className = "";
        emptyCount += !rNum;
        invalidCount += rNum < 1 || rNum > 9;

        // Check columns.
        let cNum = getNum(numbers[i + j * 9]);
        colHasColllision = colHasColllision || colSet[cNum];
        colSet[cNum] = true;

        // Check 3x3 boxes.
      }

      // Highlight the UI based on whether the row/column/box had repeats.
      if (rowHasColllision || colHasColllision || boxHasColllision) {
        for (let j = 0; j < 9; j++) {
          if (rowHasColllision) {
            let p = numbers[i * 9 + j].parentElement;
            p.className = addErrorClass(p.className);
          }

          if (colHasColllision) {
            let p = numbers[i + j * 9].parentElement;
            p.className = addErrorClass(p.className);
          }

          if (boxHasColllision) {

          }
        }
      }
    }
  });
});
