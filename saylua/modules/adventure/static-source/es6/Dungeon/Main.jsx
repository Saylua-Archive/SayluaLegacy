import Inferno from "inferno";
import { createStore, applyMiddleware, compose } from 'redux';

import { getInitialGameState, logState, CoreReducer } from "./Reducers/CoreReducer";
import { addAdditionalDebugParameters } from "./Reducers/DebugReducer";
import DungeonClient from "./Components/DungeonClient";
import DebugTools from "./Components/DebugTools";

// Common events that will be ingested by the Engine every loop.
window.queue = {
  'log': [],
  'actorAttack': [],
  'actorEvent': [],
  'actorMove': [],
  'playerMove': []
};

// Does what you think it does. Handles rare, hookable events.
window.specialEventQueue = {
  'nextGameState': undefined,
  'summonEntity': undefined
};

// This is here primarily so that random sections of code know debug values.
window._getStoreState = (store) => () => store.getState();
window.getStoreState = () => false;


export default function Main() {
  getInitialGameState().then((initialState) => {
    initialState = addAdditionalDebugParameters(initialState);

    // Initialize the Redux developer tools, if possible.
    const reduxCompose = (window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__) ? window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__({ "shouldRecordChanges": false }) : false;
    const composeEnhancers = reduxCompose || compose;

    let store = createStore(CoreReducer, initialState, composeEnhancers(
      applyMiddleware(logState)
    ));

    // Initialize getStoreState with our store so that
    // the game can query for debug values.
    window.getStoreState = window._getStoreState(store);

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
