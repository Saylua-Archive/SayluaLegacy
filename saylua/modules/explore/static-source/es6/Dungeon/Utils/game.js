import * as EngineUtils from "./engine";
import { VIEWPORT_HEIGHT, VIEWPORT_WIDTH } from "../Core/Game";

const obstructions = [
  'wall'
];

export function translatePlayerLocation(player, tileLayer, tileSet, direction) {
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
    goalCell = tileLayer[g_y][g_x];
  } catch (e) {
    return player.location;
  }

  if (goalCell === undefined) {
    return player.location;
  }

  // Determine if we can go there, physically.
  goalTile = tileSet.filter((tile) => tile.id === goalCell.tile)[0];
  tileType = goalTile['type'];

  if (obstructions.indexOf(tileType) !== -1) {
    return player.location;
  }

  return [g_x, g_y];
}


// Not a pure function because we're not sadistic bastards.
// Not pure and not located within the core code because we ARE sadistic bastards.
// Or I am, at least.
export function renderMap(entitySet, entityLayer, tileSet, tileLayer, tileSprites) {

  let entityLookupTable = [];

  for (let entity of entityLayer) {
    let x = entity.location.x;
    let y = entity.location.y;

    entityLookupTable[y] = entityLookupTable[y] || [];
    entityLookupTable[y][x] = entityLookupTable[y][x] || [];

    entityLookupTable[y][x].push(entity);
  }

  // Locate the player, determine map size.
  let player = entityLayer[0];

  let p_x = player.location.x;
  let p_y = player.location.y;

  let mapHeight = tileLayer.length;
  let mapWidth = tileLayer[0].length;

  // Define mapView bounds
  // Keeps two points within the bounds of the map, and a minimum distance from each other.
  // Points 'a'[x, y] and 'b'[x, y] define the top left and bottom right corners of our visible 'viewport' tiles.

  let a_x, b_x, x_pool;
  x_pool = VIEWPORT_WIDTH - 1;

  a_x = Math.max(p_x - Math.round(VIEWPORT_WIDTH / 2), 0);                                  // console.log(`a_x is ${a_x}`);
  x_pool -= (p_x - a_x);                                                    // console.log(`Units left in the pool: is ${x_pool}`);
  b_x = Math.min(p_x + x_pool, VIEWPORT_WIDTH - 1);             // console.log(`b_x is ${b_x}`);
  x_pool -= (b_x - p_x);                                                    // console.log(`Units left in the pool: is ${x_pool}`);
  a_x = (b_x === VIEWPORT_WIDTH - 1) ? (a_x - x_pool) : (a_x + x_pool);     // console.log(`Adding ${x_pool} to a_x makes: ${a_x}`);

  let a_y, b_y, y_pool;
  y_pool = VIEWPORT_HEIGHT - 1;

  a_y = Math.max(p_y - Math.round(VIEWPORT_HEIGHT / 2), 0);
  y_pool -= (p_y - a_y);
  b_y = Math.min(p_y + y_pool, VIEWPORT_HEIGHT - 1);
  y_pool -= (b_y - p_y);
  a_y = (b_y === VIEWPORT_HEIGHT - 1) ? (a_y - y_pool) : (a_y + y_pool);

  // Provide ourselves with some utility functions.
  let within_x_bounds = (x) => (a_x <= x) && (x <= b_x);
  let within_y_bounds = (y) => (a_y <= y) && (y <= b_y);

  // There are MUCH prettier ways to do this.
  // This, however, is the fastest. Blame Javascript's expensive array operations.
  for (let _y = 0; _y < mapHeight; _y++) {
    for (let _x = 0; _x < mapWidth; _x++) {
      var currentTile = tileLayer[_y][_x];

      // Is this tile in our viewport?
      if (within_x_bounds(_x) && within_y_bounds(_y)) {
        // Normalize, then translate our (x, y) coords into a linear integer.
        let normal_x = _x - a_x;
        let normal_y = _y - a_y;

        // This is a source of slowness. Fix this if performance becomes an issue.
        let parentTile = tileSet.filter((tile) => {
          return tile.id == currentTile.tile;
        })[0];

        let linearPosition = normal_x + (VIEWPORT_WIDTH * normal_y);
        tileSprites[linearPosition].texture = EngineUtils.getTexture(parentTile.slug);
      }
    }
  }
}
