/*eslint no-console: ["off"]*/
import cloneDeep from "lodash.clonedeep";
import Reqwest from "reqwest";

import * as GameUtils from "../Utils/game";


// GameStore -> Required by DungeonClient.
// --------------------------------------
// Primary game client reducer.

export function getInitialGameState() {
  return Reqwest({
    "url": '/explore/api/generate_dungeon',
    "type": 'json',
    "method": 'post',
    "error": (error) => {
      console.log("Error contacting the Dungeon API.");
    }
  });
}

export const GameReducer = (state, action) => {
  switch (action.type) {
    case 'MOVE_PLAYER':
      var player = cloneDeep(state.entityLayer[0]);
      var entities = state.entityLayer.slice(1);
      var [p_x, p_y] = GameUtils.translatePlayerLocation(player, state.tileLayer, state.tileSet, action.direction);

      player.location.x = p_x;
      player.location.y = p_y;

      entities.unshift(player);

      return { ...state, 'entityLayer': entities };
    default:
      return state;
  }
};
