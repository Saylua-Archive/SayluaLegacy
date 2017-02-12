import onDomReady from "ondomready";
import Inferno from "inferno";

import BlocksInterface from "./BlocksInterface";
import GameState from "./GameState";


let gameState = new GameState();

onDomReady(function () {
  Inferno.render(
    <BlocksInterface model={ gameState } />,
    document.getElementById("blocks-mount")
  );
});
