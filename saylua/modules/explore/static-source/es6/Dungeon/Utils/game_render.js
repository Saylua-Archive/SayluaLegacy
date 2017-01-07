import * as GameHelpers from "./game_helpers";
import * as EngineUtils from "./engine";

import { VIEWPORT_HEIGHT, VIEWPORT_WIDTH } from "../Core/Game";


// This provides the common data layer necessary for other rendering functions to operate.
export function getBaseData(player, tileSet, tileLayer, dimensions) {
  // Calculate valid tiles.
  let validTiles = GameHelpers.calculateFOV(player.location, tileSet, tileLayer);

  // Calculate our map dimensions
  let mapHeight = tileLayer.length;
  let mapWidth = tileLayer[0].length;

  // Use map dimensions and player location to generate helper functions that tell us when a cell is in view.
  let [topLeft, bottomRight, within_x_bounds, within_y_bounds] = GameHelpers.getBounds(player.location, mapHeight, mapWidth);

  return {
    dimensions,

    validTiles,

    mapHeight,
    mapWidth,

    topLeft,
    bottomRight,
    within_x_bounds,
    within_y_bounds
  };
}


export function renderViewport(baseData, tileSet, tileLayer, tileSprites) {
  // There are MUCH prettier ways to do this.
  // This, however, is the fastest. Blame Javascript's expensive array operations.
  for (let y = 0; y < baseData.mapHeight; y++) {
    for (let x = 0; x < baseData.mapWidth; x++) {
      var currentTile = tileLayer[y][x];

      // Is this tile in our viewport?
      if (baseData.within_x_bounds(x) && baseData.within_y_bounds(y)) {
        // Set cell visibility, if necessary.
        // Why would you write this? Masochists and code hygienists. For opposite reasons, of course.
        let tileVisible = (baseData.validTiles[y] === undefined) ? false : ( (baseData.validTiles[y][x] === true) ? true : false );
        let tileSeen = (currentTile.meta.seen === true);

        // We must 'reveal' tiles, initially. We never unset this.
        if (tileVisible === true) {
          currentTile.meta.seen = true;
        }

        currentTile.meta.visible = tileVisible;

        // Normalize, then translate our (x, y) coords into a linear integer.
        let normal_x = x - baseData.topLeft.x;
        let normal_y = y - baseData.topLeft.y;

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
}


export function renderEntities(baseData, entityLayer, entitySprites) {
  entityLayer.map((entity, i) => {
    let x = entity.location.x;
    let y = entity.location.y;

    let sprite = entitySprites[i];

    let [stageWidth, stageHeight] = baseData.dimensions;

    let tileHeight = (stageHeight / VIEWPORT_HEIGHT);
    let tileWidth = (stageWidth / VIEWPORT_WIDTH);

    let verticalOffSet = tileHeight * 0.1;
    let horizontalOffset = tileWidth * 0.1;

    // We've got a winner!
    if (baseData.within_x_bounds(x) && baseData.within_y_bounds(y)) {
      // Set entity visibility, if necessary
      let entityVisible = (baseData.validTiles[y] === undefined) ? false : ( (baseData.validTiles[y][x] === true) ? true : false );
      let entitySeen = (entity.meta.seen === true);

      if (entityVisible) {
        entity.meta.seen = true;
        entity.location.lastSeen = {x, y};
      }

      if (entityVisible === true) {
        // Normalize our (x, y) coords
        let normal_x = x - baseData.topLeft.x;
        let normal_y = y - baseData.topLeft.y;

        sprite.alpha = 1;
        sprite.x = Math.round((normal_x * tileWidth) + horizontalOffset);
        sprite.y = Math.round((normal_y * tileHeight) + verticalOffSet);
        sprite.visible = true;
      } else {
        if (entitySeen === true) {
          // Normalize our (x, y) coords
          let normal_x = entity.location.lastSeen.x - baseData.topLeft.x;
          let normal_y = entity.location.lastSeen.y - baseData.topLeft.y;

          sprite.alpha = 0.4;
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


export function renderMinimap(baseData, tileSet, tileLayer, minimapSprites) {
  for (let y = 0; y < baseData.mapHeight; y++) {
    for (let x = 0; x < baseData.mapWidth; x++) {
      var currentTile = tileLayer[y][x];

      // Why would you write this? Masochists and code hygienists. For opposite reasons, of course.
      let tileVisible = (baseData.validTiles[y] === undefined) ? false : ( (baseData.validTiles[y][x] === true) ? true : false );
      let tileSeen = (currentTile.meta.seen === true);

      let parentTile = tileSet[currentTile.tile];

      // All we have to do is change the texture of the sprite map, as the number of sprites never changes.
      let linearPosition = x + (baseData.mapWidth * y);
      let sprite = minimapSprites[linearPosition];

      // Now, we change the tile state depending on whether or not we can see it, and whether or not we /have/ seen it.
      let baseVisibility = 0.8;

      if (tileVisible) {
        sprite.alpha = 1 * baseVisibility;
        sprite.texture = EngineUtils.getTexture(parentTile.slug);
      } else {
        if (tileSeen) {
          sprite.alpha = 0.5 * baseVisibility;
          sprite.texture = EngineUtils.getTexture(parentTile.slug);
        } else {
          sprite.alpha = 1 * baseVisibility;
          sprite.texture = EngineUtils.getTexture('tile_fog');
        }
      }
    }
  }
}
