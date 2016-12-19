import * as GameUtils from "../Utils/game";
import * as MathUtils from "../Utils/math";

export const VIEWPORT_HEIGHT = 18;
export const VIEWPORT_WIDTH = 32;

export default class Game {
  constructor(renderWidth, renderHeight, store) {
    // Store store
    this.store = store.getState();

    // Store store store store.
    this.unsubscribe = store.subscribe(() => {
      this.store = store.getState();
      this.state.shouldReRender = true;
    });

    // Initialize Pixi renderer
    this.renderer = PIXI.autoDetectRenderer(renderWidth, renderHeight);

    // Create a stage for us to draw to.
    this.stage = new PIXI.Container();

    // Tile layer sub-stage
    this.tileStage = new PIXI.Container();
    this.stage.addChild(this.tileStage);

    // Entity layer sub-stage
    this.entityStage = new PIXI.Container();
    this.stage.addChild(this.entityStage);
    this.entityStage.interactive = true;
    this.entityStage.on('click', this.test.bind(this));
    this.entityStage.on('tap', this.test.bind(this));

    this.state = {
      "dimensions": [renderWidth, renderHeight],
      "shouldReRender": true,
      "tileSprites": this.generateTileSprites(renderWidth, renderHeight)
    };

    this.state.tileSprites.map((sprite) => {
      this.tileStage.addChild(sprite);
    });
    this.test();
  }

  getRenderer() {
    return this.renderer.view;
  }

  generateTileSprites(stageWidth, stageHeight) {
    // Initialize window textures if necessary.
    window.textures = window.textures || {};
    window.textures['null'] = PIXI.Texture.fromImage("/static/img/tiles/test/null.png");

    let spriteLayer = [];
    let nullTexture = window.textures['null'];

    let spriteHeight = stageHeight / VIEWPORT_HEIGHT;
    let spriteWidth = stageWidth / VIEWPORT_WIDTH;

    console.log(`view ${spriteHeight}px ${spriteWidth}px`);

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

  test() {
    let sprite = new PIXI.Sprite.fromImage("/static/img/loxi.png");
    let [width, height] = this.state.dimensions;

    sprite.x = MathUtils.randomRange(0, width);
    sprite.y = MathUtils.randomRange(0, height);

    sprite.height = 150;
    sprite.width = 150;

    this.entityStage.addChild(sprite);
  }

  loop() {
    if (this.state.shouldReRender === true) {
      console.log("THE WORLD HAS CHANGED");

      // Edit our tilemap in place.
      GameUtils.renderMap(
        this.store.entitySet,
        this.store.entityLayer,
        this.store.tileSet,
        this.store.tileLayer,
        this.state.tileSprites
      );

      this.state.shouldReRender = false;
    }

    this.renderer.render(this.stage);
  }
}
