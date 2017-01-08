import Inferno from "inferno";
import InfernoDOM from "inferno-dom";
import { createStore, applyMiddleware } from 'redux';

import { getInitialGameState, logState, GameReducer } from "./Reducers/GameReducer";
import DungeonClient from "./Components/DungeonClient";
import DebugTools from "./Components/DebugTools";


export default function Main() {
  getInitialGameState().then((initialState) => {
    console.log(initialState);
    let store = createStore(GameReducer, initialState, applyMiddleware(logState));

    InfernoDOM.render(
      <DungeonClient store={ store } />,
      document.getElementById("dungeon-client-mount")
    );

    InfernoDOM.render(
      <DebugTools store={ store } />,
      document.getElementById("dungeon-debug-mount")
    );
  });
}

Main();
