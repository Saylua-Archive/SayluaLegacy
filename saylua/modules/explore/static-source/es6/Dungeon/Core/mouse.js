// mouse -> Required by Core/GameRenderer
// --------------------------------------
// Mouse related game interactions.

import * as Graphics from "./graphics";


export function tileHover(mouseSprites, context) {
  let handler = (mouseSprites, context) => (event) => {
    let sprite = event.currentTarget;
    let tileSeen = (sprite.meta.tile !== 'fog');
    let isPathable = (sprite.meta.tile_is_obstruction === false);

    let queuedSummon = window.getStoreState().debug.queuedSummon;
    let debugSummonerActive = (queuedSummon !== false);

    // If the debug summoner is active, show the master hand and a preview sprite.
    if (debugSummonerActive === true) {
      sprite.defaultCursor = 'url(\'/static/img/dungeons/debug/master_hand_grab.png\') 23 28, auto';

      mouseSprites[1].texture = Graphics.getTexture(queuedSummon.id);
      mouseSprites[1].x = sprite.x;
      mouseSprites[1].y = sprite.y;

      mouseSprites[1].visible = true;
    } else {
      mouseSprites[1].texture = window.textures['null'];
      mouseSprites[1].visible = false;
    }

    // Debug summoner

    // No hover effects for unseen tiles or obstructions.
    if (tileSeen && isPathable) {
      // Is there an enemy within the currently hovered location?
      let matchingEntity = context.gameState.entityLayer.filter((entity) => (
        (entity.parent !== '0x1000') &&
        (entity.location.x === sprite.meta.grid_x) &&
        (entity.location.y === sprite.meta.grid_y)
      ));

      if (matchingEntity.length > 0) {
        mouseSprites[0].texture = Graphics.getTexture("interface_tile_hover_red");
      } else {
        mouseSprites[0].texture = Graphics.getTexture("interface_tile_hover_green");
      }

      if (debugSummonerActive === false) {
        sprite.defaultCursor = 'pointer';
      }

      mouseSprites[0].x = sprite.x;
      mouseSprites[0].y = sprite.y;
      mouseSprites[0].visible = true;
    } else {
      if (debugSummonerActive === false) {
        sprite.defaultCursor = 'inherit';
      }
      mouseSprites[0].visible = false;
    }
  };

  return handler(mouseSprites, context);
}


export function tileClick(context) {
  let handler = (context) => (event) => {
    let queuedSummon = window.getStoreState().debug.queuedSummon;
    let debugSummonerActive = (queuedSummon !== false);
    let sprite = event.currentTarget;

    if (debugSummonerActive === true) {
      context.store.dispatch({
        'type': 'DEBUG_PLACE_SUMMON',
        'location': {
          "x": sprite.meta.grid_x,
          "y": sprite.meta.grid_y
        }
      });
    }
  };

  return handler(context);
}
