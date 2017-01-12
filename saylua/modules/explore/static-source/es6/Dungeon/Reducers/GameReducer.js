/* eslint { no-redeclare: 0 } */
import cloneDeep from "lodash.clonedeep";
import Reqwest from "reqwest";
import astar from "astar";


import * as EngineScripting from "../Utils/engine_scripting";
import * as GameLogic from "../Utils/game_logic";
import * as EngineUtils from "../Utils/engine";

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
      result.nodeGraph = new astar.Graph(EngineUtils.generateNodeGraph(result.tileSet, result.tileLayer), { diagonal: true });
      result.gameClock = 0;
      result.UI = {
        "showMinimap": false
      };
      result.log = [];
    }
  });
}

/**
  Perhaps this will be useful in the future for when more than one type of action can move time forward.
  e.g. ranged attacks, 'waiting', using items.
**/
/*export const processAI = store => next => action => {
  // Ensure that if the player moves, all scripted objects resolve their behaviors.
  if (action.type === 'MOVE_PLAYER') {
    store.dispatch({ 'type': 'PROCESS_AI' });
  }

  // Continue as usual.
  let result = next(action);
  return result;
};*/

export const logState = store => next => action => {
  // Before any action, make sure we update from the log queue.
  // This is really not kosher at all.

  // Note that this does not log in real-time, it occurs one step afterwards in game-time.
  if (window.logQueue !== undefined) {
    if ((window.logQueue.length > 0) && (window.logging !== true)) {
      window.logging = true;

      let newEvents = window.logQueue.slice();
      store.dispatch({ 'type': 'LOG_EVENTS', 'events': newEvents });

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
    case 'PROCESS_AI':
      var t0 = performance.now();

      var [entities, tiles] = GameLogic.processAI(state.tileSet, state.tileLayer, state.entitySet, state.entityLayer, state.nodeGraph);

      var t1 = performance.now();
      console.log("Process AI took " + (t1 - t0) + " milliseconds.");

      return { ...state, 'entityLayer': entities, 'tileLayer': tiles };

    case 'HOOK_ENTER':

      // Entities will always affect tiles before the reverse occurs.
      // Fixable, but not immediately necessary for them to be simultaneous.
      var [entities, tiles] = EngineScripting.resolveActions({
        'actionType': action.type,
        'actionLocation': action.location,
        'nodeGraph': state.nodeGraph,
        'tileSet': state.tileSet,
        'tileLayer': state.tileLayer.slice(),
        'entitySet': state.entitySet,
        'entityLayer': state.entityLayer.slice()
      });

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

      // All of the below is highly experimental. Questionable syntax.
      var newState = { ...state, 'entityLayer': entities, 'gameClock': newGameClock };

      // Make sure we trigger any entity / tile we collide with
      newState = GameReducer(newState, { 'type': 'HOOK_ENTER', 'location': player.location });

      // Step the game forward one time unit
      newState = GameReducer(newState, { 'type': 'PROCESS_AI' });

      return newState;

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
