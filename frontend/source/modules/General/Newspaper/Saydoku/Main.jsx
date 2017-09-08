import React, { Component } from 'react';

import './Saydoku.scss';

export default class Saydoku extends Component {
  constructor(props) {
    super(props);
    this.puzzle = Array(9).fill(0).map(() => {
      return Array(9).fill(0);
    });
  }

  checkPuzzle(e) {
    this.checkPuzzle = true;
  }

  render() {
    let puzzle = this.puzzle;
    let errors = this.errorMatrix;
    let checkPuzzle = this.checkPuzzle;
    return (
      <div>
        <h2>
          The Daily Saydoku Puzzle
        </h2>
        <table id="puzzle-container">
          <tbody>
          {
            puzzle.map((row, i) => {
              return (
                <tr>
                  {
                    row.map((square, j) => {
                      let numberClass = "puzzle-number";
                      if (checkPuzzle) {
                        // TODO: Replace with real error checking.
                        let errorCount = 1;
                        numberClass += " puzzle-error-" + errorCount;
                      }
                      if (square) {
                        return<td><span className={ numberClass }>{ square }</span></td>;
                      }
                      return <td><input className={ numberClass } type="text" maxLength="1" /></td>;
                    })
                  }
                </tr>
              );
            })
          }
          </tbody>
        </table>
        <div>
          <h3>The Rules</h3>
          <div className="newspaper-side-box">
            Fill the whole board with numbers 1-9 while following these rules:
            <ul>
              <li>
                No number can appear twice in a single row or column.
              </li>
              <li>
                None of the 3x3 subsections of the board can have repeated numbers either.
              </li>
            </ul>
          </div>
        </div>
        <div>
          <div className="newspaper-side-box">
            Everyday, thousands of Sayluans complete the Sayluan Gazette's daily Saydoku
            puzzle and send in their solutions to earn a prize.
          </div>
        </div>
        <button id="puzzle-submit" onClick={ this.checkPuzzle.bind(this) }>
          Check Solution
        </button>
      </div>
    );
  }
}
