// debug -> Required by Reducers/DebugReducer
// --------------------------------------
// Useful functions for the debug reducer.
import { uuid } from "Utils";

export function revealMap(tileLayer, entityLayer) {
  for (let tile of tileLayer) {
    tile.meta.seen = true;
  }

  for (let entity of entityLayer) {
    entity.meta.seen = true;
    entity.location.lastSeen = {
      'x': entity.location.x,
      'y': entity.location.y
    };
  }

  return [tileLayer, entityLayer];
}

export function updateItemSets(summon, entitySet, tileSet) {
  let isTile = summon.id.startsWith("tile");

  if (isTile === true) {
    if (tileSet[summon.id] === undefined) {
      tileSet[summon.id] = summon;
    }
  } else {
    if (entitySet[summon.id] === undefined) {
      entitySet[summon.id] = summon;
    }
  }

  return [entitySet, tileSet];
}


export function placeSummon(summon, location, entityLayer, tileLayer) {
  let isTile = summon.id.startsWith('tile');

  if (isTile === true) {
    let matchingTile = tileLayer.filter((tile) => (
      tile.location.x === location.x &&
      tile.location.y === location.y
    ))[0];

    matchingTile.tile = summon.id;
    matchingTile.meta = {};
  } else {
    entityLayer.push({
      "id": uuid(),
      "meta": {
        "health": (summon.meta.maxHP !== undefined) ? summon.meta.maxHP : 100
      },
      "parent": summon.id,
      "location": {
        "x": location.x,
        "y": location.y
      }
    });
  }

  return [entityLayer, tileLayer];
}
