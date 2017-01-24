// DebugReducer -> Required by Reducers/CoreReducer.
// --------------------------------------
// Debug data / functions for Dungeons.
import { getInitialGameState } from "./CoreReducer";


export function addAdditionalDebugParameters(state) {
  let debug = {
    "FOVEnabled": true
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

    default:
      return state;
  }
};
