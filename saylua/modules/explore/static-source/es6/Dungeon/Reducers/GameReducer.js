/*eslint no-console: ["off"]*/
import cloneDeep from "lodash.clonedeep";
import Reqwest from "reqwest";

import * as EngineScripting from "../Utils/engine_scripting";
import * as GameLogic from "../Utils/game_logic";


// GameStore -> Required by DungeonClient.
// --------------------------------------
// Primary game client reducer.

export function getInitialGameState() {
  return Reqwest({
    "url": '/explore/api/generate_dungeon',
    "type": 'json',
    "method": 'post',
    "error": (error) => {
      throw("Error contacting the Dungeon API.");
    },
    "success": (result) => {
      let newTileSet = {};
      result.tileSet.map((tile) => {
        newTileSet[tile.id] = tile;
      });

      let newEntitySet = {};
      result.entitySet.map((entity) => {
        newEntitySet[entity.id] = entity;
      });

      result.tileSet = newTileSet;
      result.entitySet = newEntitySet;
      result.gameClock = 0;
      result.eventsQueue = [];
      result.UI = {
        "showMinimap": false
      };
      result.log = [];
    }
  });
}

export const logState = store => next => action => {
  // Before any action, make sure we update from the log queue.
  // This is really not kosher at all.

  // Also, make the state available for debugging in the window.
  window.debugState = store.getState();

  // Note that this does not log in real-time, it occurs one step afterwards in game-time.
  if (window.logQueue !== undefined) {
    if ((window.logQueue.length > 0) && (window.logging !== true)) {
      window.logging = true;

      let newEvents = window.logQueue.slice();
      store.dispatch({'type': 'LOG_EVENTS', 'events': newEvents});

      window.logQueue = [];
      window.logging = false;
    }
  }

  // Continue as usual.
  let result = next(action);
  return result;
};

export const GameReducer = (state, action) => {
  switch (action.type) {
    case 'HOOK_ENTER':

      // Entities will always affect tiles before the reverse occurs.
      // Fixable, but not immediately necessary for them to be simultaneous.
      var [entities, tiles] = EngineScripting.resolveActions(
        action.type,
        action.location,
        state.tileSet,
        state.tileLayer,
        state.entitySet,
        state.entityLayer
      );

      return { ...state, 'entityLayer': entities, 'tileLayer': tiles };

    case 'MOVE_PLAYER':

      var player = cloneDeep(state.entityLayer[0]);
      var entities = state.entityLayer.slice().slice(1);
      var translation = GameLogic.translatePlayerLocation(player, state.tileLayer, state.tileSet, action.direction);
      var playerMoved = (player.location != translation);

      player.location = translation;
      entities.unshift(player);

      // Advance game clock by 1 if the player actually moved.
      var newGameClock = state.gameClock;
      newGameClock = playerMoved ? newGameClock + 1 : newGameClock;

      // Highly experimental. Questionable syntax.
      var newState = { ...state, 'entityLayer': entities, 'gameClock': newGameClock };
      return GameReducer(newState, { 'type': 'HOOK_ENTER', 'location': player.location });

    case 'LOG_EVENTS':

      // This is safe, .concat apparently operates on a copy. JS. So inconsistent.
      var newLog = state.log.concat(action.events);

      return { ...state, 'log': newLog };

    case 'TOGGLE_MINIMAP':

      var showMinimap = !state.UI.showMinimap;
      var newUIState = { ...state.UI, 'showMinimap': showMinimap };

      return { ...state, 'UI': newUIState };

    default:
      return state;
  }
};
