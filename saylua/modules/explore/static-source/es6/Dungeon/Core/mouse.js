// mouse -> Required by Core/GameRenderer
// --------------------------------------
// Mouse related game interactions.

import * as Graphics from "./graphics";


export function tileHover(mouseSprites, context) {
  let handler = (mouseSprites, context) => (event) => {
    let sprite = event.currentTarget;
    let tileSeen = (sprite.meta.tile !== 'fog');
    let isPathable = (sprite.meta.tile_is_obstruction === false);

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

      sprite.defaultCursor = 'pointer';
      mouseSprites[0].x = sprite.x;
      mouseSprites[0].y = sprite.y;
      mouseSprites[0].visible = true;
    } else {
      sprite.defaultCursor = 'inherit';
      mouseSprites[0].visible = false;
    }
  };

  return handler(mouseSprites, context);
}
