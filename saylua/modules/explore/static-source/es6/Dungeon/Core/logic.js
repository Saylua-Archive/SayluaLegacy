// logic -> Required by Reducers/GameReducer
// --------------------------------------
// Pure functions that calculate complex interactions
// between given inputs for the GameReducer.

import * as MathUtils from "../Utils/math";
import * as FOVUtils from "../Utils/fov";

import { interpretGameEvents } from "./scripting";
import { VIEWPORT_HEIGHT, VIEWPORT_WIDTH, VISION_RADIUS } from "./GameRenderer";

export const OBSTRUCTIONS = [
  'wall'
];

const MAXIMUM_ENTITY_PROCESSING_DISTANCE = Math.floor(VISION_RADIUS * 3);
const MAXIMUM_TILE_PROCESSING_DISTANCE = Math.floor(VISION_RADIUS * 1.2);


export function calculateFOV(location, tileSet, tileLayer, mapWidth) {
  let validTiles = [];

  let visitTile = (x, y) => {
    validTiles[y] = validTiles[y] || [];
    validTiles[y][x] = true;
  };

  let isBlocked = (x, y) => {
    let linearGlobalPosition = ((y * mapWidth) + x);
    let parentTileID = tileLayer[linearGlobalPosition].tile;
    let parentTileType = tileSet[parentTileID].type;
    return (OBSTRUCTIONS.indexOf(parentTileType) !== -1);
  };

  FOVUtils.calculateFOV(location.x, location.y, VISION_RADIUS, visitTile, isBlocked);

  return validTiles;
}


export function getBounds(player_location, mapHeight, mapWidth) {
  let p_x = player_location.x;
  let p_y = player_location.y;

  // Define mapView bounds
  // Keeps two points within the bounds of the map, and a minimum distance from each other.
  // Points 'a'[x, y] and 'b'[x, y] define the top left and bottom right corners of our visible 'viewport' tiles.

  let a_x, b_x, x_pool;
  x_pool = VIEWPORT_WIDTH - 1;

  a_x = Math.max(p_x - Math.round(VIEWPORT_WIDTH / 2), 0);                  //console.log(`a_x is ${a_x}`);
  x_pool -= (p_x - a_x);                                                    //console.log(`Units left in the pool: ${x_pool}`);
  b_x = Math.min(p_x + x_pool, mapWidth - 1);                               //console.log(`b_x is ${b_x}`);
  x_pool -= (b_x - p_x);                                                    //console.log(`Units left in the pool: is ${x_pool}`);
  a_x = (b_x === mapWidth - 1) ? (a_x - x_pool) : (a_x + x_pool);           //console.log(`Adding ${x_pool} to a_x makes: ${a_x}`);

  let a_y, b_y, y_pool;
  y_pool = VIEWPORT_HEIGHT - 1;

  a_y = Math.max(p_y - Math.round(VIEWPORT_HEIGHT / 2), 0);                 //console.log(`a_y is ${a_y}`);
  y_pool -= (p_y - a_y);                                                    //console.log(`Units left in the pool: ${y_pool}`);
  b_y = Math.min(p_y + y_pool, mapHeight - 1);                              //console.log(`b_y is ${b_y}`);
  y_pool -= (b_y - p_y);                                                    //console.log(`Units left in the pool: ${y_pool}`);
  a_y = (b_y === mapHeight - 1) ? (a_y - y_pool) : (a_y + y_pool);          //console.log(`Adding ${y_pool} to a_y makes: ${a_y}`);

  // Provide ourselves with some utility functions.
  let within_x_bounds = (x) => (a_x <= x) && (x <= b_x);
  let within_y_bounds = (y) => (a_y <= y) && (y <= b_y);

  // Coords
  let topLeft = { 'x': a_x, 'y': a_y };
  let bottomRight = { 'x': b_x, 'y': b_y };

  return [ topLeft, bottomRight, within_x_bounds, within_y_bounds ];
}


export function translatePlayerLocation(player, tileLayer, tileSet, entityLayer, direction, mapWidth) {
  let p_x, p_y, g_x, g_y, goalCell, goalTile, tileType;

  p_x = player.location.x;
  p_y = player.location.y;

  g_x = p_x;
  g_y = p_y;

  switch(direction) {
    case 'up':
      g_y = p_y - 1;
      break;
    case 'down':
      g_y = p_y + 1;
      break;
    case 'left':
      g_x = p_x - 1;
      break;
    case 'right':
      g_x = p_x + 1;
      break;
  }

  // Determine if we can visit this tile, theoretically.
  try {
    let linearPosition = ((g_y * mapWidth) + g_x);
    goalCell = tileLayer[linearPosition];
    let validTile = (goalCell.location.x === g_x && goalCell.location.y === g_y);
    if (!validTile) {
      throw("Invalid location");
    }
  } catch (e) {
    return player.location;
  }

  if (goalCell === undefined) {
    return player.location;
  }

  // Determine if we can go there, physically.
  goalTile = tileSet[goalCell.tile];
  tileType = goalTile['type'];

  if (OBSTRUCTIONS.indexOf(tileType) !== -1) {
    return player.location;
  }

  // One last check, is there an entity on this tile? (This should trigger an attack in the future)
  let targetEntity = entityLayer.filter((entity) => (
    (entity.location.x === g_x) &&
    (entity.location.y === g_y) &&
    (entity.meta.dead !== true)
  ));

  if (targetEntity.length > 0) {
    return {
      'x': player.location.x,
      'y': player.location.y,
      'target': targetEntity[0]
    };
  }

  return { "x": g_x, "y": g_y };
}


export function processAI(tileSet, tileLayer, entitySet, entityLayer, nodeGraph, mapWidth) {
  let playerLocation = entityLayer[0].location;
  let distanceFromPlayer = (newLocation) => {
    return MathUtils.distance(playerLocation, newLocation);
  };

  let referenceEntityLayer = entityLayer;
  let newEntityLayer = entityLayer.slice();
  let newTileLayer = tileLayer.slice();

  // Note that this operates from a copy.
  for (let entity of referenceEntityLayer) {

    // Does this entity still exist?
    // Entities have to determine whether or not they still exist due to cross-interactions.
    let matchingEntity = newEntityLayer.filter((_entity) => (
      (_entity.id == entity.id) &&
      (_entity.meta.dead !== true)
    ));

    if (matchingEntity.length > 0) {
      matchingEntity = matchingEntity[0];

      // Is this entity worth actually processing? These operations are expensive, you know.
      if (distanceFromPlayer(matchingEntity.location) < MAXIMUM_ENTITY_PROCESSING_DISTANCE) {
        [newEntityLayer, newTileLayer] = interpretGameEvents({
          'actionType': 'TRIGGER_EVENT_IDLE',
          'target': matchingEntity,
          'tileSet': tileSet,
          'tileLayer': newTileLayer,
          'entitySet': entitySet,
          'entityLayer': newEntityLayer,
          'nodeGraph': nodeGraph,
          'mapWidth': mapWidth
        });
      }
    }
  }

  for (let tile of newTileLayer) {
    // Should we script this tile?
    if (distanceFromPlayer(tile.location) < MAXIMUM_TILE_PROCESSING_DISTANCE) {
      [newEntityLayer, newTileLayer] = interpretGameEvents({
        'actionType': 'TRIGGER_EVENT_IDLE',
        'target': tile,
        'tileSet': tileSet,
        'tileLayer': newTileLayer,
        'entitySet': entitySet,
        'entityLayer': newEntityLayer,
        'mapWidth': mapWidth
      });
    }
  }

  return [newEntityLayer, newTileLayer];
}
