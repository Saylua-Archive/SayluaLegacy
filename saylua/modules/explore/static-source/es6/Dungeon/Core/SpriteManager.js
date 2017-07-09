// SpriteManager -> Required by Components/GameRenderer
// --------------------------------------
// Contrary to what the name implies, the only sprites this
// manager handles are entity sprites. No others.
//
// Provides some common courtesy access and manipulation
// to the GameRenderer's entity sprites and entity stage.

import * as Graphics from "./graphics";
import { TILE_SIZE } from "./GameRenderer";


export const generateSprite = (entity) => {
  let spriteTexture = Graphics.getTexture(entity.parent);
  let sprite = new PIXI.Sprite(spriteTexture);

  sprite.entityID = entity.id;
  sprite.parentID = entity.parent;

  sprite.visible = false;
  sprite.height = TILE_SIZE * 0.8;
  sprite.width = TILE_SIZE * 0.8;

  return sprite;
};


export default class SpriteManager {
  constructor(store, entityStage) {
    // Store store
    this.store = store;

    // Store store store
    this.gameState = this.store.getState();

    // Store store store store.
    // This will be triggered any time the store state changes.
    this.unsubscribe = this.store.subscribe(() => {
      this.gameState = store.getState();
    });

    // Store sprite stage.
    this.entityStage = entityStage;

    this.state = {};
  }


  get children() {
    return this.entityStage.children;
  }


  cleanup() {
    this.entityStage.removeChildren();
  }


  generateSprite(entity) {
    return generateSprite(entity);
  }


  getSprite(entityID) {
    let items = this.entityStage.children.filter((sprite) => {
      return sprite.entityID === entityID;
    });

    if (items.length > 1) {
      throw("Attempting to find a sprite returned more than one matching item.");
    } else if (items.length === 1) {
      return items[0];
    }

    return false;
  }


  addSprite(items) {
    items = (items.length === undefined) ? [items] : items;

    for (let item of items) {
      this.entityStage.addChild(item);
    }
  }


  removeSprite(entityID) {
    let item = this.getSprite(entityID);

    if (item !== false) {
      this.entityStage.removeChild(item);
    }

    return (item !== false);
  }
}
