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


export function generateMinimapSprites(stageWidth, stageHeight, mapWidth, mapHeight) {
  // Initialize window textures if necessary.
  window.textures = window.textures || {};
  window.textures['null'] = PIXI.Texture.fromImage("/static/img/tiles/test/null.png");

  let spriteLayer = [];
  let nullTexture = window.textures['null'];

  // What is the smallest size with which we can contain the entire map within the viewport, proportionally?
  // Let us also make sure it is 40% the size of the viewport at it's largest dimension.
  let size = 25; // size, in px

  // There are probably much more efficient ways to do this.
  while ( ((size * mapHeight) > (stageHeight * 0.4)) || ((size * mapWidth) > (stageWidth * 0.4)) ) {
    size = size - 0.1;
  }

  size = Math.floor(size * 10) / 10;

  // Place our map 10% from the top right
  let horizontalOffset = (stageWidth - (size * mapWidth)) / 1.1;
  let verticalOffset = (stageHeight - (size * mapHeight)) * 0.1;

  for (let row = 0; row < mapHeight; row++) {
    for (let col = 0; col < mapWidth; col++) {
      let sprite = new PIXI.Sprite(nullTexture);

      sprite.height = size;
      sprite.width = size;

      sprite.x = (col * size) + horizontalOffset;
      sprite.y = (row * size) + verticalOffset;

      spriteLayer.push(sprite);
    }
  }

  return spriteLayer;
}
