/*eslint no-console: ["off"]*/
import cloneDeep from "lodash.clonedeep";
import Reqwest from "reqwest";

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
      result.UI = {
        "showMinimap": false
      };
    }
  });
}


export const GameReducer = (state, action) => {
  switch (action.type) {
    case 'MOVE_PLAYER':

      var player = cloneDeep(state.entityLayer[0]);
      var entities = state.entityLayer.slice(1);
      var translation = GameLogic.translatePlayerLocation(player, state.tileLayer, state.tileSet, action.direction);

      player.location = translation;
      entities.unshift(player);

      return { ...state, 'entityLayer': entities };

    case 'TOGGLE_MINIMAP':
      var showMinimap = !state.UI.showMinimap;
      var newUIState = { ...state.UI, 'showMinimap': showMinimap };
      return { ...state, 'UI': newUIState };

    default:
      return state;
  }
};
