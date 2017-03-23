// mouse -> Required by Core/GameRenderer
// --------------------------------------
// Mouse related game interactions.

import cloneDeep from "lodash.clonedeep";

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

      // Make sure this value is actively updated for viewport zooming.
      context.state.panOffset = {
        "x": -(adjusted_x),
        "y": -(adjusted_y)
      };
    }
  };

  return handler(context);
}


export function tileHover(mouseSprites, context) {
  let handler = (mouseSprites, context) => (event) => {
    // Do not process while the viewport is panning.
    if (context.state.currentlyDragging === true) {
      mouseSprites[0].visible = false;
      mouseSprites[1].visible = false;

      return;
    }

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

    // Debugging
    let TILE_SIZE_SCALED = TILE_SIZE * context.state.zoomLevel;
    let x = Math.round(sprite.meta.grid_x * TILE_SIZE_SCALED);
    let y = Math.round(sprite.meta.grid_y * TILE_SIZE_SCALED);
    console.log(`Tile Position: ${ x } : ${ y }`);

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


export function viewportZoom(className, context) {
  const getDeltaY = (event) => {
    return (event.wheelDelta && !event.deltaY) ? event.wheelDelta * -1 : event.deltaY;
  };

  // Grab element, determine which event we need to use to capture mouse scroll.
  let scrollEvent = 'onwheel' in document ? 'wheel' : 'mousewheel';
  let viewportEl = document.querySelector(className);

  // Bind a map zoom to our viewport element.
  viewportEl.addEventListener(scrollEvent, (event) => {
    event.preventDefault();

    // Grab our adjusted Delta value to determine scroll direction.
    let delta = getDeltaY(event);

    let priorZoom = cloneDeep(context.state.zoomLevel);

    // Set our new Zoom level based on scroll direction
    if (delta == -100) {
      context.state.zoomLevel = Math.min(1.4, context.state.zoomLevel + 0.02);
    } else if (delta == 100) {
      context.state.zoomLevel = Math.max(0.6, context.state.zoomLevel - 0.02);
    }

    // Update 'World' scale ratio.
    context.state.stages.world.primary.scale.set(context.state.zoomLevel);

    // Update Stages.HUD.mouse scale ratio.
    for (let mouseSprite of context.state.sprites.HUD.mouse) {
      mouseSprite.height = (TILE_SIZE * context.state.zoomLevel);
      mouseSprite.width = (TILE_SIZE * context.state.zoomLevel);
    }

    // Track to the mouse's position as we scroll.
    let zoomChanged = (priorZoom !== context.state.zoomLevel);
    if (zoomChanged === true) {
      context.updateScreenPosition();
    }
  });
}
