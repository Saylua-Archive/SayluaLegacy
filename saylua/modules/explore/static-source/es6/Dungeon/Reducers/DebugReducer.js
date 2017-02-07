// DebugReducer -> Required by Reducers/CoreReducer.
// --------------------------------------
// Debug data / functions for Dungeons.

import { getInitialGameState } from "./CoreReducer";
import * as Debug from "../Core/debug";


export function addAdditionalDebugParameters(state) {
  let debug = {
    "FOVEnabled": true,
    "keyboardInputEnabled": true
  };

  return {...state, debug };
}


export const DebugReducer = (state, action) => {
  switch (action.type) {

    case 'DEBUG_REGENERATE_DUNGEON':
      getInitialGameState(true).then((initialState) => {
        window.nextGameState = addAdditionalDebugParameters(initialState);
      });

      var newUIState = { ...state.UI, 'waitingOnDungeonRequest': true };
      return { ...state, 'UI': newUIState };

    case 'DEBUG_REVEAL_MAP':
      var entityLayer = state.entityLayer.slice();
      var tileLayer = state.tileLayer.slice();

      var [newTileLayer, newEntityLayer] = Debug.revealMap(tileLayer, entityLayer);

      return { ...state, 'tileLayer': newTileLayer, 'entityLayer': newEntityLayer };

    case 'DEBUG_TOGGLE_OPTION':
      var newDebug = { ...state.debug };
      newDebug[action.name] = !newDebug[action.name];

      return { ...state, 'debug': newDebug };

    default:
      return state;
  }
};
