import Inferno from "inferno";
import InfernoDOM from "inferno-dom";

import BlocksInterface from "./BlocksInterface";
import GameState from "./GameState";


let gameState = new GameState();

window.addEventListener("load", function () {
  InfernoDOM.render(
    <BlocksInterface model={ gameState } />,
    document.getElementById("blocks-mount")
  );
});
