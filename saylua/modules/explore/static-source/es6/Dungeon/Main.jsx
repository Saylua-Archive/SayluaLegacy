import Inferno from "inferno";
import InfernoDOM from "inferno-dom";
import { createStore } from 'redux';

import { getInitialGameState, GameReducer } from "./Reducers/GameReducer";
import DungeonClient from "./Components/DungeonClient";
import DebugTools from "./Components/DebugTools";


export default function Main() {
  getInitialGameState().then((initialState) => {
    let store = createStore(GameReducer, initialState);

    Inferno.render(
      <DungeonClient store={ store } />,
      document.getElementById("dungeon-client-mount")
    );

    Inferno.render(
      <DebugTools store={ store } />,
      document.getElementById("dungeon-debug-mount")
    );
  });
}

Main();
