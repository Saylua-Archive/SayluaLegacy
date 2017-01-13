import * as EngineFOV from "./engine_fov";
import { VIEWPORT_HEIGHT, VIEWPORT_WIDTH, VISION_RADIUS } from "../Core/Game";


// This could perhaps be located in a better place.
export const OBSTRUCTIONS = [
  'wall'
];


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

  EngineFOV.calculateFOV(location.x, location.y, VISION_RADIUS, visitTile, isBlocked);

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
