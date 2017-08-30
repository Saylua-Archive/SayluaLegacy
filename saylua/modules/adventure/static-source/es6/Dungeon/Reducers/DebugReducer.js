/* eslint { no-redeclare: 0 } */
// DebugReducer -> Required by Reducers/CoreReducer.
// --------------------------------------
// Debug data / functions for Dungeons.

import cloneDeep from "lodash.clonedeep";

import { getInitialGameState } from "./CoreReducer";
import * as Debug from "../Core/debug";


export function addAdditionalDebugParameters(state) {
  let debug = {
    "enableUpdateTimers": false,
    "FOVEnabled": true,
    "keyboardInputEnabled": true,
    "queuedSummon": false,
    "showCollisions": false
  };

  return { ...state, debug };
}


export const DebugReducer = (state, action) => {
  switch (action.type) {
    case 'DEBUG_PLACE_SUMMON':
      var [newEntityLayer, newTileLayer] = Debug.placeSummon(
        state.debug.queuedSummon,
        action.location,
        state.entityLayer.slice(),
        state.tileLayer.slice(),
        state.nodeGraph
      );

      return { ...state, 'tileLayer': newTileLayer, 'entityLayer': newEntityLayer };

    case 'DEBUG_REGENERATE_DUNGEON':
      getInitialGameState(true).then((initialState) => {
        window.specialEventQueue.nextGameState = addAdditionalDebugParameters(initialState);
      });

      var newUIState = { ...state.UI, 'waitingOnDungeonRequest': true };
      return { ...state, 'UI': newUIState };

    case 'DEBUG_REVEAL_MAP':
      var [newTileLayer, newEntityLayer] = Debug.revealMap(state.tileLayer.slice(), state.entityLayer.slice());

      return { ...state, 'tileLayer': newTileLayer, 'entityLayer': newEntityLayer };

    case 'DEBUG_TOGGLE_OPTION':
      var newDebug = { ...state.debug };
      newDebug[action.name] = !newDebug[action.name];

      return { ...state, 'debug': newDebug };

    case 'DEBUG_QUEUE_SUMMON':
      var newEntitySet, newTileSet;

      if (action.summon === false) {
        newEntitySet = state.entitySet;
        newTileSet = state.tileSet;
      } else {
        [newEntitySet, newTileSet] = Debug.updateItemSets(action.summon, cloneDeep(state.entitySet), cloneDeep(state.tileSet));
      }

      var newDebug = { ...state.debug, queuedSummon: action.summon };

      return { ...state, 'entitySet': newEntitySet, 'tileSet': newTileSet, 'debug': newDebug };

    case 'DEBUG_SHOW_COLLISIONS':
      var newDebug = { ...state.debug, 'showCollisions': true };

      return { ...state, 'debug': newDebug };

    default:
      return state;
  }
};
