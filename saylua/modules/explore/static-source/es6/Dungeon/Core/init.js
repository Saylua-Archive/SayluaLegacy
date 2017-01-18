// game_init -> Required by Core/GameRenderer
// --------------------------------------
// Primal functions that generate initial game data.
// Only run once.

import * as Graphics from "./graphics";

import { OBSTRUCTIONS } from "./logic";
import { VIEWPORT_HEIGHT, VIEWPORT_WIDTH } from "./GameRenderer";


/******************************** RENDERER INIT ***********************************/


export function generateEntitySprites(stageWidth, stageHeight, entityLayer, entitySet) {
  // Initialize window textures if necessary.
  window.textures = window.textures || {};
  window.textures['null'] = PIXI.Texture.fromImage("/static/img/tiles/test/null.png");

  let spriteLayer = [];
  let spriteHeight = (stageHeight / VIEWPORT_HEIGHT) * 0.8;
  let spriteWidth = (stageWidth / VIEWPORT_WIDTH) * 0.8;

  for (let entity of entityLayer) {
    let entityParent = entitySet[entity.parent];
    let spriteTexture = Graphics.getTexture(entityParent.slug);
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

export function generateHUDSprites(data) {
  let playerStatusSprites = generatePlayerStatusSprites();
  let miniMapSprites = generateMinimapSprites(data);
  let actionButtons = [];

  return {
    'actionButtons': actionButtons,
    'miniMap': miniMapSprites,
    'playerStatus': playerStatusSprites
  };
}

function generateMinimapSprites(data) {
  // Initialize window textures if necessary.
  window.textures = window.textures || {};
  window.textures['null'] = PIXI.Texture.fromImage("/static/img/tiles/test/null.png");

  let spriteLayer = [];
  let nullTexture = window.textures['null'];

  // What is the smallest size with which we can contain the entire map within the viewport, proportionally?
  // Let us also make sure it is 40% the size of the viewport at it's largest dimension.
  let size = 25; // size, in px

  // There are probably much more efficient ways to do this.
  while ( ((size * data.mapHeight) > (data.renderHeight * 0.4)) || ((size * data.mapWidth) > (data.renderWidth * 0.4)) ) {
    size = size - 0.1;
  }

  size = Math.floor(size * 10) / 10;

  // Place our map 10% from the top right
  let horizontalOffset = (data.renderWidth - (size * data.mapWidth)) / 1.1;
  let verticalOffset = (data.renderHeight - (size * data.mapHeight)) * 0.1;

  for (let row = 0; row < data.mapHeight; row++) {
    for (let col = 0; col < data.mapWidth; col++) {
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

function generatePlayerStatusSprites() {
  // This is lame, but calculating sizes before the canvas has rendered is difficult.
  const HPtextureSize = { 'height': 193, 'width': 1186 };

  let heartsTexture = Graphics.getTexture("interface_hp_positive");
  let maskTexture = Graphics.getTexture("interface_hp_negative");
  let hearts = new PIXI.Sprite(heartsTexture);
  let mask = new PIXI.Sprite(maskTexture);
  let fill = new PIXI.Graphics();

  let calculatedHeight = ((HPtextureSize.height * 300) / HPtextureSize.width);
  let calculatedWidth = 300;

  hearts.x = 25;
  hearts.y = 25;
  mask.x = 25;
  mask.y = 25;

  hearts.height = calculatedHeight;
  hearts.width = calculatedWidth;
  mask.height = calculatedHeight;
  mask.width = calculatedWidth;

  //fill.beginFill(0xde3232);
  fill.beginFill(0xff5a97);
  fill.drawRect(25, 25, 300, 75);
  fill.mask = mask;
  fill.alpha = 0.7;

  window.fill = fill;

  // The order is important here, due to z-indexing.
  return [fill, hearts, mask];
}


/******************************** REDUCER INIT ***********************************/


export function generateNodeGraph(tileSet, tileLayer) {
  let nodeGraph = [];

  // Our A* implementation uses [x][y] grids, so we must convert from our [y][x] grids.
  // Weight based on whether or not they are obstructions.
  for (let tile of tileLayer) {
    nodeGraph[tile.location.x] = nodeGraph[tile.location.x] || [];

    let parentTileType = tileSet[tile.tile].type;
    let isObstruction = (OBSTRUCTIONS.indexOf(parentTileType) !== -1);

    if (isObstruction) {
      nodeGraph[tile.location.x].push(0);
    } else {
      nodeGraph[tile.location.x].push(1);
    }
  }

  return nodeGraph;
}


export function normalizeTileLayer(tileLayer) {
  let mapHeight = tileLayer.length;
  let mapWidth = tileLayer[0].length;
  let normalizedTileLayer = [];

  for (let y = 0; y < mapHeight; y++) {
    for (let x = 0; x < mapWidth; x++) {
      let tile = tileLayer[y][x];

      tile.location = { x, y };
      normalizedTileLayer.push(tile);
    }
  }

  return [mapHeight, mapWidth, normalizedTileLayer];
}
