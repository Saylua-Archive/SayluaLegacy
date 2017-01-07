import * as GameRender from "../Utils/game_render";
import * as GameInit from "../Utils/game_init";
import * as MathUtils from "../Utils/math";

export const VIEWPORT_HEIGHT = 18;
export const VIEWPORT_WIDTH = 32;


export default class Game {
  constructor(renderWidth, renderHeight, store) {
    // Store store
    this.store = store.getState();

    // Store store store store.
    // This will be triggered any time the store state changes.
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

    // Create HUD sub-stage and it's own sub-stages.
    this.HUDStage = new PIXI.Container();

    this.miniMap = new PIXI.Container();
    this.playerStatus = new PIXI.Container();
    this.gameLog = new PIXI.Container();
    this.actionButtons = new PIXI.Container();

    this.HUDStage.addChild(this.miniMap);
    this.HUDStage.addChild(this.playerStatus);
    this.HUDStage.addChild(this.gameLog);
    this.HUDStage.addChild(this.actionButtons);

    this.stage.addChild(this.entityStage);

    // Final testing / debug layer.
    this.testLayer = new PIXI.Container();
    this.stage.addChild(this.testLayer);
    this.testLayer.interactive = true;
    this.testLayer.on('click', this.test.bind(this));
    this.testLayer.on('tap', this.test.bind(this));

    this.state = {
      "dimensions": [renderWidth, renderHeight],
      "shouldReRender": true,
      "tileSprites": GameInit.generateTileSprites(renderWidth, renderHeight),
      "entitySprites": GameInit.generateEntitySprites(
        renderWidth,
        renderHeight,
        this.store.entityLayer,
        this.store.entitySet
      ),
    };

    this.state.tileSprites.map((sprite) => {
      this.tileStage.addChild(sprite);
    });
    this.state.entitySprites.map((sprite) => {
      this.entityStage.addChild(sprite);
    });
    this.test();
  }


  getRenderer() {
    return this.renderer.view;
  }


  test() {
    let sprite = new PIXI.Sprite.fromImage("/static/img/loxi.png");
    let [width, height] = this.state.dimensions;

    sprite.x = MathUtils.randomRange(0, width);
    sprite.y = MathUtils.randomRange(0, height);

    sprite.height = 150;
    sprite.width = 150;

    this.testLayer.addChild(sprite);
  }


  loop() {
    if (this.state.shouldReRender === true) {
      console.log("THE WORLD HAS CHANGED");

      let player = this.store.entityLayer[0];
      let baseData = GameRender.getBaseData(
        player,
        this.store.tileSet,
        this.store.tileLayer,
        this.state.dimensions
      );

      // Edit our sprite layers in-place. So gross.

      GameRender.renderViewport(
        baseData,
        this.store.tileSet,
        this.store.tileLayer,
        this.state.tileSprites
      );

      GameRender.renderEntities(
        baseData,
        this.store.entityLayer,
        this.state.entitySprites
      );

      this.state.shouldReRender = false;
    }

    this.renderer.render(this.stage);
  }
}
