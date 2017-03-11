import Inferno from "inferno";

import BlocksInterface from "./BlocksInterface";
import GameState from "./GameState";


let gameState = new GameState();

Inferno.render(
  <BlocksInterface model={ gameState } />,
  document.getElementById("blocks-mount")
);
