import Inferno from "inferno";
import InfernoDOM from "inferno-dom";
import { createStore, applyMiddleware, compose } from 'redux';

import { getInitialGameState, logState, GameReducer } from "./Reducers/GameReducer";
import DungeonClient from "./Components/DungeonClient";
import DebugTools from "./Components/DebugTools";


export default function Main() {
  getInitialGameState().then((initialState) => {

    // We do this for the Redux chrome extension.
    const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;
    let store = createStore(GameReducer, initialState, composeEnhancers(
      applyMiddleware(logState)
    ));

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
