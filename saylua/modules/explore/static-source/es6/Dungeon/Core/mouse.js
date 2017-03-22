// mouse -> Required by Core/GameRenderer
// --------------------------------------
// Mouse related game interactions.

import * as Graphics from "./graphics";

import { TILE_SIZE } from "./GameRenderer";


export function panDragStart(context) {
  let handler = (context) => (event) => {
    context._dragOrigin = {
      "x": event.data.global.x,
      "y": event.data.global.y
    };

    context._dragReference = {
      "x": context.state.stages.world.primary.position.x,
      "y": context.state.stages.world.primary.position.y
    };

    context.state.currentlyDragging = true;
  };

  return handler(context);
}


export function panDragEnd(context) {
  let handler = (context) => (event) => {
    context._dragOrigin = null;
    context._dragReference = null;

    context.state.currentlyDragging = false;
  };

  return handler(context);
}


export function panDragMove(context) {
  let handler = (context) => (event) => {
    if (context.state.currentlyDragging === true) {
      let difference_x = context._dragOrigin.x - event.data.global.x;
      let difference_y = context._dragOrigin.y - event.data.global.y;

      let adjusted_x = context._dragReference.x - difference_x;
      let adjusted_y = context._dragReference.y - difference_y;

      context.state.stages.world.primary.position.set(adjusted_x, adjusted_y);
    }
  };

  return handler(context);
}


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
      sprite.toGlobal(context.state.stages.primary.position, mouseSprites[1].position);

      mouseSprites[1].visible = true;
    } else {
      mouseSprites[1].texture = window.textures['null'];
      mouseSprites[1].visible = false;
    }

    // If the tile is a pathable and visible, display a highlighted tile border.
    if (tileSeen && isPathable) {
      // Is there an enemy within the currently hovered location?
      let matchingEntity = context.gameState.entityLayer.filter((entity) => (
        (entity.parent !== '0x1000') &&
        (entity.location.x === sprite.meta.grid_x) &&
        (entity.location.y === sprite.meta.grid_y)
      ));

      // Switch tile border to red or green based on whether or not we see an enemy.
      if (matchingEntity.length > 0) {
        mouseSprites[0].texture = Graphics.getTexture("interface_tile_hover_red");
      } else {
        mouseSprites[0].texture = Graphics.getTexture("interface_tile_hover_green");
      }

      // Switch to a hover cursor, if the debugger hasn't already changed it to the Master Hand.
      if (debugSummonerActive === false) {
        sprite.defaultCursor = 'pointer';
      }

      // Update tilesprite position and make it visible.
      sprite.toGlobal(context.state.stages.primary.position, mouseSprites[0].position);
      mouseSprites[0].visible = true;
    } else {
      // Reset cursor to it's default state if hovered over an invalid tile
      // while the debugger is inactive.
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


export function viewportZoom(context) {
  let handler = (context) => (event) => {
    if (event.direction === "up") {
      context.state.zoomLevel = Math.min(1.4, context.state.zoomLevel + 0.1);
    } else if (event.direction === "down") {
      context.state.zoomLevel = Math.max(0.6, context.state.zoomLevel - 0.1);
    }

    context.state.stages.world.primary.scale.set(context.state.zoomLevel);

    for (let mouseSprite of context.state.sprites.HUD.mouse) {
      mouseSprite.height = (TILE_SIZE * context.state.zoomLevel);
      mouseSprite.width = (TILE_SIZE * context.state.zoomLevel);
    }

    context.updateScreenPosition();
  };

  return handler(context);
}
