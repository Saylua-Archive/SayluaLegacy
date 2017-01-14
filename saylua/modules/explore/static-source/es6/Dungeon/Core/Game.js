import * as GameRender from "../Utils/game_render";
import * as GameInit from "../Utils/game_init";
import * as MathUtils from "../Utils/math";

import Engine from "./Engine";

export const VIEWPORT_HEIGHT = 18;
export const VIEWPORT_WIDTH = 32;
export const VISION_RADIUS = 8;


export default class Game {
  constructor(renderWidth, renderHeight, store) {
    // Store store
    this.store = store.getState();

    this.updateCounter = 0;

    // Store store store store.
    // This will be triggered any time the store state changes.
    this.unsubscribe = store.subscribe(() => {
      this.updateCounter += 1;
      this.store = store.getState();
      //this.miniMap.visible = this.store.UI.showMinimap;
      this.miniMap.visible = true;

      this.state.gameStateChanged = true;

      // Use this to measure how long it takes for each game update to process when the player moves.
      // Corresponding start is located in `DungeonClient.jsx`
      window.framet0 = window.framet0 || performance.now();
      window.framet1 = performance.now();
      let timeElapsed = Math.floor((window.framet1 - window.framet0) * 100) / 100;

      window.average = window.average || 0;
      window.average = Math.floor(((window.average + timeElapsed) / 2) * 100) / 100;
      console.log(`This update took ${ timeElapsed } milliseconds. Average: ${ window.average }ms`);
    });

    // Engine, mostly responsible for scripts and realtime animations.
    this.engine = new Engine(store);

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

    this.stage.addChild(this.HUDStage);

    // Final testing / debug layer.
    this.testLayer = new PIXI.Container();
    this.stage.addChild(this.testLayer);
    this.testLayer.interactive = true;
    this.testLayer.on('click', this.test.bind(this));
    this.testLayer.on('tap', this.test.bind(this));

    // Generate the various sprite layers necessary.
    let tileSprites = GameInit.generateTileSprites(
      renderWidth,
      renderHeight
    );

    let entitySprites = GameInit.generateEntitySprites(
      renderWidth,
      renderHeight,
      this.store.entityLayer,
      this.store.entitySet
    );

    let HUDSprites = GameInit.generateHUDSprites({
      renderWidth,
      renderHeight,
      'mapWidth': this.store.mapWidth, // Total map width
      'mapHeight': this.store.mapHeight // Total map height
    });

    this.state = {
      "dimensions": [renderWidth, renderHeight],
      "gameStateChanged": true,
      tileSprites,
      entitySprites,
      HUDSprites
    };


    // Final stage setup
    this.state.tileSprites.map((sprite) => {
      this.tileStage.addChild(sprite);
    });
    this.state.entitySprites.map((sprite) => {
      this.entityStage.addChild(sprite);
    });
    this.state.HUDSprites.miniMap.map((sprite) => {
      this.miniMap.addChild(sprite);
    });
    this.state.HUDSprites.playerStatus.map((sprite) => {
      this.playerStatus.addChild(sprite);
    });


    this.miniMap.visible = false;
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
    let player = this.store.entityLayer[0];

    if (this.state.gameStateChanged === true) {
      let baseData = GameRender.getBaseData(
        player,
        this.store.tileSet,
        this.store.tileLayer,
        this.state.dimensions,
        this.store.mapHeight,
        this.store.mapWidth
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

      GameRender.renderMinimap(
        baseData,
        this.store.tileSet,
        this.store.tileLayer,
        this.state.HUDSprites.miniMap
      );

      this.state.gameStateChanged = false;
    }

    GameRender.renderHUD(player, this.state.HUDSprites);

    this.renderer.render(this.stage);
  }
}
