import * as EngineUtils from "./engine";
import { VIEWPORT_HEIGHT, VIEWPORT_WIDTH } from "../Core/Game";

const OBSTRUCTIONS = [
  'wall'
];

function calculateFOV(location, tileSet, tileLayer) {
  let validTiles = [];

  let visitTile = (x, y) => {
    validTiles[y] = validTiles[y] || [];
    validTiles[y][x] = true;
  };

  let isBlocked = (x, y) => {
    let currentTile = tileLayer[y][x].tile;
    let tileType = tileSet[currentTile].type;
    return (OBSTRUCTIONS.indexOf(tileType) !== -1);
  };

  EngineUtils.calculateFOV(location.x, location.y, 8, visitTile, isBlocked);

  return validTiles;
}

export function generateEntitySprites(stageWidth, stageHeight, entityLayer, entitySet) {
  // Initialize window textures if necessary.
  window.textures = window.textures || {};
  window.textures['null'] = PIXI.Texture.fromImage("/static/img/tiles/test/null.png");

  let spriteLayer = [];
  let spriteHeight = (stageHeight / VIEWPORT_HEIGHT) * 0.8;
  let spriteWidth = (stageWidth / VIEWPORT_WIDTH) * 0.8;

  for (let entity of entityLayer) {
    let entityParent = entitySet[entity.parent];
    let spriteTexture = EngineUtils.getTexture(entityParent.slug);
    let sprite = new PIXI.Sprite(spriteTexture);

    sprite.visible = false;
    sprite.height = spriteHeight;
    sprite.width = spriteWidth;

    spriteLayer.push(sprite);
  }

  return spriteLayer;
}

export function generateTileSprites(stageWidth, stageHeight) {
  // Initialize window textures if necessary.
  window.textures = window.textures || {};
  window.textures['null'] = PIXI.Texture.fromImage("/static/img/tiles/test/null.png");

  let spriteLayer = [];
  let nullTexture = window.textures['null'];

  let spriteHeight = stageHeight / VIEWPORT_HEIGHT;
  let spriteWidth = stageWidth / VIEWPORT_WIDTH;

  for (let row = 0; row < VIEWPORT_HEIGHT; row++) {
    for (let col = 0; col < VIEWPORT_WIDTH; col++) {
      let sprite = new PIXI.Sprite(nullTexture);

      sprite.height = spriteHeight;
      sprite.width = spriteWidth;

      sprite.x = (col * spriteWidth);
      sprite.y = (row * spriteHeight);

      spriteLayer.push(sprite);
    }
  }

  return spriteLayer;
}

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
  goalTile = tileSet[goalCell.tile];
  tileType = goalTile['type'];

  if (OBSTRUCTIONS.indexOf(tileType) !== -1) {
    return player.location;
  }

  return { "x": g_x, "y": g_y };
}


// Not a pure function because we're not sadistic bastards.
// Not pure and not located within the core code because we ARE sadistic bastards.
// Or I am, at least.
export function renderMap(entitySet, entityLayer, tileSet, tileLayer, tileSprites, entitySprites, dimensions) {
  // Locate the player, determine map size.
  let player = entityLayer[0];

  let p_x = player.location.x;
  let p_y = player.location.y;

  // Calculate valid tiles.
  let validTiles = calculateFOV(player.location, tileSet, tileLayer);

  let mapHeight = tileLayer.length;
  let mapWidth = tileLayer[0].length;

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

  // There are MUCH prettier ways to do this.
  // This, however, is the fastest. Blame Javascript's expensive array operations.
  for (let y = 0; y < mapHeight; y++) {
    for (let x = 0; x < mapWidth; x++) {
      var currentTile = tileLayer[y][x];

      // Is this tile in our viewport?
      if (within_x_bounds(x) && within_y_bounds(y)) {
        // Set cell visibility, if necessary.
        // Why would you write this? Masochists and code hygienists. For opposite reasons, of course.
        let tileVisible = (validTiles[y] === undefined) ? false : ( (validTiles[y][x] === true) ? true : false );
        let tileSeen = (currentTile.meta.seen === true);

        // We must 'reveal' tiles, initially. We never unset this.
        if (tileVisible === true) {
          currentTile.meta.seen = true;
        }

        currentTile.meta.visible = tileVisible;

        // Normalize, then translate our (x, y) coords into a linear integer.
        let normal_x = x - a_x;
        let normal_y = y - a_y;

        let parentTile = tileSet[currentTile.tile];

        // All we have to do is change the texture of the sprite map, as the number of sprites never changes.
        let linearPosition = normal_x + (VIEWPORT_WIDTH * normal_y);
        let sprite = tileSprites[linearPosition];

        // Now, we change the tile state depending on whether or not we can see it, and whether or not we /have/ seen it.
        if (tileVisible) {
          sprite.alpha = 1;
          sprite.texture = EngineUtils.getTexture(parentTile.slug);
        } else {
          if (tileSeen) {
            sprite.alpha = 0.5;
            sprite.texture = EngineUtils.getTexture(parentTile.slug);
          } else {
            sprite.alpha = 1;
            sprite.texture = EngineUtils.getTexture('tile_fog');
          }
        }
      }
    }
  }

  // Finally, render entities.
  entityLayer.map((entity, i) => {
    let x = entity.location.x;
    let y = entity.location.y;

    let sprite = entitySprites[i];

    let [stageWidth, stageHeight] = dimensions;

    let tileHeight = (stageHeight / VIEWPORT_HEIGHT);
    let tileWidth = (stageWidth / VIEWPORT_WIDTH);

    let verticalOffSet = (stageHeight / VIEWPORT_HEIGHT) * 0.1;
    let horizontalOffset = (stageWidth / VIEWPORT_HEIGHT) * 0.1;

    // We've got a winner!
    if (within_x_bounds(x) && within_y_bounds(y)) {
      // Set entity visibility, if necessary
      let entityVisible = (validTiles[y] === undefined) ? false : ( (validTiles[y][x] === true) ? true : false );
      let entitySeen = (entity.meta.seen === true);

      if (entityVisible) {
        entity.meta.seen = true;
        entity.location.lastSeen = {x, y};
      }

      if (entityVisible === true) {
        // Normalize our (x, y) coords
        let normal_x = x - a_x;
        let normal_y = y - a_y;

        sprite.alpha = 1;
        sprite.x = Math.round((normal_x * tileWidth) + horizontalOffset);
        sprite.y = Math.round((normal_y * tileHeight) + verticalOffSet);
        sprite.visible = true;
      } else {
        if (entitySeen === true) {
          // Normalize our (x, y) coords
          let normal_x = entity.location.lastSeen.x - a_x;
          let normal_y = entity.location.lastSeen.y - a_y;

          sprite.alpha = 0.5;
          sprite.x = Math.round((normal_x * tileWidth) + horizontalOffset);
          sprite.y = Math.round((normal_y * tileHeight) + verticalOffSet);
          sprite.visible = true;
        }
      }
    } else {
      // AHUEAHUEHAUEHEHEUHAHEUEAHUEHEHEHEHEAHEAHEHE
      // YOU'LL NEVER SEE YOUR FAMILY EVER AGAIN
      sprite.visible = false;
    }
  });
}
