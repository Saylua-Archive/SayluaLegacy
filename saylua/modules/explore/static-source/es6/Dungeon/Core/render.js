// render -> Required by Core/GameRenderer
// --------------------------------------
// Dirty functions related to mutating sprite layers
// to assist the game renderer.

import * as Graphics from "./graphics";

import { TILE_SIZE } from "./GameRenderer";
import { calculateFOV, getBounds, OBSTRUCTIONS } from "./logic";


// This provides the common data layer necessary for other rendering functions to operate.
export function getBaseData(player, tileSet, tileLayer, dimensions, mapHeight, mapWidth, zoomScale, panOffset) {
  // Calculate valid tiles.
  let validTiles = calculateFOV(player.location, tileSet, tileLayer, mapWidth);

  // Helper function to tell us when a cell is in view.
  let tileVisible = getBounds(player.location, mapHeight, mapWidth, zoomScale, panOffset);

  return {
    dimensions,

    validTiles,

    mapHeight,
    mapWidth,

    tileVisible
  };
}


export function generateEntitySprite(dimensions, entityParentID) {
  let spriteHeight = (TILE_SIZE * 0.8);
  let spriteWidth = (TILE_SIZE * 0.8);

  let spriteTexture = Graphics.getTexture(entityParentID);
  let sprite = new PIXI.Sprite(spriteTexture);

  sprite.visible = false;
  sprite.height = spriteHeight;
  sprite.width = spriteWidth;

  return sprite;
}


export function renderViewport(baseData, tileSet, tileLayer, tileSprites) {
  // There are MUCH prettier ways to do this.
  // This, however, is the fastest. Blame Javascript's expensive array operations.
  for (let tile of tileLayer) {
    // Reasons
    let x = tile.location.x;
    let y = tile.location.y;

    // Is this tile in our viewport?
    if (baseData.tileVisible(x, y)) {

      // Set cell visibility, if necessary.
      let FOVEnabled = window.getStoreState().debug.FOVEnabled;
      let tileVisible;

      if (FOVEnabled === true) {
        // Why would you write this? Masochists and code hygienists. For opposite reasons, of course.
        tileVisible = (baseData.validTiles[y] === undefined) ? false : ( (baseData.validTiles[y][x] === true) ? true : false );
      } else {
        tileVisible = true;
      }

      let tileSeen = (tile.meta.seen === true);

      // We must 'reveal' tiles, initially. We never unset this.
      if (tileVisible === true) {
        tile.meta.seen = true;
      }

      tile.meta.visible = tileVisible;

      let parentTile = tileSet[tile.tile];

      let linearPosition = x + (baseData.mapWidth * y);
      let sprite = tileSprites[linearPosition];

      // Store this data for later use.
      sprite.meta.tile = tile.id;
      sprite.meta.tile_is_obstruction = (OBSTRUCTIONS.indexOf(parentTile.type) !== -1);
      sprite.meta.grid_x = x;
      sprite.meta.grid_y = y;

      // Now, we change the tile state depending on whether or not we can see it, and whether or not we /have/ seen it.
      if (tileVisible) {
        sprite.alpha = 1;
        sprite.texture = Graphics.getTexture(parentTile.id);
      } else {
        if (tileSeen) {
          sprite.alpha = 0.5;
          sprite.texture = Graphics.getTexture(parentTile.id);
        } else {
          // Reasons
          sprite.meta.tile = 'fog';

          sprite.alpha = 1;
          sprite.texture = Graphics.getTexture('tile_fog');
        }
      }
    }
  }
}


export function renderEntities(baseData, entityLayer, entitySprites, generateEntitySprite) {
  entityLayer.map((entity, i) => {
    let x = entity.location.x;
    let y = entity.location.y;

    let sprite = entitySprites[i] || generateEntitySprite(entity.parent);

    let tileHeight = TILE_SIZE;
    let tileWidth = TILE_SIZE;

    let verticalOffSet = tileHeight * 0.1;
    let horizontalOffset = tileWidth * 0.1;

    // Is the sprite alive?
    if (entity.meta.dead === true) {
      sprite.visible = false;
      return;
    }

    // We've got a winner!
    if (baseData.tileVisible(x, y)) {
      // Set entity visibility, if necessary
      let FOVEnabled = window.getStoreState().debug.FOVEnabled;
      let entityVisible;

      if (FOVEnabled === true) {
        entityVisible = (baseData.validTiles[y] === undefined) ? false : ( (baseData.validTiles[y][x] === true) ? true : false );
      } else {
        entityVisible = true;
      }

      let entitySeen = (entity.meta.seen === true);

      if (entityVisible === true) {
        entity.meta.seen = true;
        entity.location.lastSeen = {x, y};
      }

      if (entityVisible === true) {
        sprite.alpha = 1;
        sprite.x = Math.round((x * tileWidth) + horizontalOffset);
        sprite.y = Math.round((y * tileHeight) + verticalOffSet);
        sprite.visible = true;
      } else {
        if (entitySeen === true) {
          // One last check. Is the last known location currently visible?
          // We don't want to render ghosts if they're looking at exactly where it was.
          let lastX = entity.location.lastSeen.x;
          let lastY = entity.location.lastSeen.y;
          let lastLocationVisible = (baseData.validTiles[lastY] === undefined) ? false : ( (baseData.validTiles[lastY][lastX] === true) ? true : false );

          if (lastLocationVisible === true) {
            sprite.visible = false;
          } else {
            sprite.alpha = 0.4;
            sprite.x = Math.round((x * tileWidth) + horizontalOffset);
            sprite.y = Math.round((y * tileHeight) + verticalOffSet);
            sprite.visible = true;
          }
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
  for (let tile of tileLayer) {
    // Reasons
    let x = tile.location.x;
    let y = tile.location.y;

    // Why would you write this? Masochists and code hygienists. For opposite reasons, of course.
    let tileVisible = (baseData.validTiles[y] === undefined) ? false : ( (baseData.validTiles[y][x] === true) ? true : false );
    let tileSeen = (tile.meta.seen === true);

    let parentTile = tileSet[tile.tile];

    // All we have to do is change the texture of the sprite map, as the number of sprites never changes.
    let linearPosition = (baseData.mapWidth * y) + x;
    let sprite = minimapSprites[linearPosition];

    // Now, we change the tile state depending on whether or not we can see it, and whether or not we /have/ seen it.
    let baseVisibility = 0.8;

    if (tileVisible) {
      sprite.alpha = 1 * baseVisibility;
      sprite.texture = Graphics.getTexture(parentTile.id);
      sprite.visible = true;
    } else {
      if (tileSeen) {
        sprite.alpha = 0.5 * baseVisibility;
        sprite.texture = Graphics.getTexture(parentTile.id);
        sprite.visible = true;
      } else {
        sprite.visible = false;
      }
    }
  }
}

export function renderHUD(player, HUDSprites) {
  renderHealth(player, HUDSprites);
}

function renderHealth(player, HUDSprites) {
  // Set proper hearts percentage.
  let fill = HUDSprites.playerStatus[0];


  /*window.debugMaxHP = window.debugMaxHP || 100;
  window.debugHP = (window.debugHP === undefined) ? 75 : window.debugHP;

  window.debugHP = (window.debugHP + 1) % window.debugMaxHP;

  player.meta.health = window.debugHP;*/

  let fillPercentage = (player.meta.health / 100);
  fill.width = (150 * fillPercentage);
}
