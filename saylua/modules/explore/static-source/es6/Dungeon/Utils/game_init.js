import * as EngineUtils from "./engine";

import { VIEWPORT_HEIGHT, VIEWPORT_WIDTH } from "../Core/Game";


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
