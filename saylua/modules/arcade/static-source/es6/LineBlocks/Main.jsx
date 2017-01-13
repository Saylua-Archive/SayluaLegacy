import Inferno from "inferno";

import BlocksInterface from "./BlocksInterface";
import GameState from "./GameState";


let gameState = new GameState();

window.addEventListener("load", function () {
  Inferno.render(
    <BlocksInterface model={ gameState } />,
    document.getElementById("blocks-mount")
  );
});
