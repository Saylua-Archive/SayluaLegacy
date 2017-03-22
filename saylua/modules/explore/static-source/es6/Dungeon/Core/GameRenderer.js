// GameRenderer -> Required by Components/DungeonClient
// --------------------------------------
// The core game loop. High level game renderer.
// This interprets the data that composes Dungeons,
// but delegates the actual logic and mutation necessary
// to do so elsewhere.

import * as MouseInteractions from "./mouse";
import * as GameRender from "./render";
import * as GameInit from "./init";

import { getScreenOffset } from "./logic";
import Engine from "./Engine";

export const TILE_SIZE = 45;
export const VISION_RADIUS = 8;


export default class GameRenderer {
  constructor(renderWidth, renderHeight, store) {
    // Store store
    this.store = store;

    // Initialize the gameState from our store.
    this.gameState = store.getState();

    this.updateCounter = 0;

    // Store store store store.
    // This will be triggered any time the store updates.
    this.unsubscribe = store.subscribe(() => {
      this.updateCounter += 1;
      this.gameState = store.getState();
      this.state.stages.HUD.miniMap.visible = this.gameState.UI.showMinimap;

      this.state.gameStateChanged = true;

      // Use this to measure how long it takes for each game update to process when the player moves.
      // Corresponding start is located in `DungeonClient.jsx`
      window.framet0 = window.framet0 || performance.now();
      window.framet1 = performance.now();
      let timeElapsed = Math.floor((window.framet1 - window.framet0) * 100) / 100;

      window.average = window.average || 0;
      window.average = Math.floor(((window.average + timeElapsed) / 2) * 100) / 100;

      if (this.gameState.debug.enableUpdateTimers === true) {
        console.log(`#${ this.gameState.gameClock }: This update took ${ timeElapsed } milliseconds. Average: ${ window.average }ms`); // eslint-disable-line no-console
      }
    });

    // Store the Animation Engine
    this.engine = new Engine(store);

    // Initialize Pixi renderer
    this.renderer = PIXI.autoDetectRenderer(renderWidth, renderHeight);

    // Create a stage for us to draw to.
    let stages = {
      "primary": new PIXI.Container(),
      "world": {
        "primary": new PIXI.Container(),

        "tiles": new PIXI.Container(),
        "entities": new PIXI.Container()
      },
      "HUD": {
        "primary": new PIXI.Container(),

        "actionButtons": new PIXI.Container(),
        "gameLog": new PIXI.Container(),
        "miniMap": new PIXI.Container(),
        "mouse": new PIXI.Container(),
        "playerStatus": new PIXI.Container()
      },
      "testing": new PIXI.Container()
    };

    // Store all of our child containers inside of our primary container.
    stages.primary.addChild(stages.world.primary);
    stages.primary.addChild(stages.HUD.primary);
    stages.primary.addChild(stages.testing);

    // Store world children inside of world primary container.
    stages.world.primary.addChild(stages.world.tiles);
    stages.world.primary.addChild(stages.world.entities);

    // Store HUD children inside of HUD primary container.
    stages.HUD.primary.addChild(stages.HUD.mouse);
    stages.HUD.primary.addChild(stages.HUD.actionButtons);
    stages.HUD.primary.addChild(stages.HUD.gameLog);
    stages.HUD.primary.addChild(stages.HUD.miniMap);
    stages.HUD.primary.addChild(stages.HUD.playerStatus);

    // Final testing / debug layer setup.
    stages.testing.interactive = true;
    stages.testing.on('click', this.test.bind(this));
    stages.testing.on('tap', this.test.bind(this));

    // Start our miniMap off hidden.
    stages.HUD.miniMap.visible = false;

    // Generate the various sprite layers necessary.
    let tileSprites = GameInit.generateTileSprites(
      this.gameState.mapHeight,
      this.gameState.mapWidth
    );

    let entitySprites = GameInit.generateEntitySprites(
      this.gameState.entityLayer,
      this.gameState.entitySet
    );

    let HUDSprites = GameInit.generateHUDSprites({
      renderWidth,
      renderHeight,
      'mapHeight': this.gameState.mapHeight, // Total map height
      'mapWidth': this.gameState.mapWidth // Total map width
    });

    let sprites = {
      "tiles": tileSprites,
      "entities": entitySprites,
      "HUD": HUDSprites
    };

    // -- Final setup

    // Mouse events
    let tileHoverHandler = MouseInteractions.tileHover(sprites.HUD.mouse, this);
    let tileClickHandler = MouseInteractions.tileClick(this);

    sprites.tiles.map((sprite) => {
      // Bind mouse events
      sprite.interactive = true;
      sprite.buttonMode = true;

      sprite.on('mousedown', tileClickHandler);
      sprite.on('mouseover', tileHoverHandler);

      // Append to the stage
      stages.world.tiles.addChild(sprite);
    });

    sprites.entities.map((sprite) => {
      stages.world.entities.addChild(sprite);
    });

    sprites.HUD.miniMap.map((sprite) => {
      stages.HUD.miniMap.addChild(sprite);
    });

    sprites.HUD.playerStatus.map((sprite) => {
      stages.HUD.playerStatus.addChild(sprite);
    });

    sprites.HUD.mouse.map((sprite) => {
      stages.HUD.mouse.addChild(sprite);
    });

    this.state = {
      "dimensions": [renderHeight, renderWidth],
      "gameStateChanged": true,
      stages,
      sprites,
      "zoomLevel": 1,
      "panOffset": { "x": 0, "y": 0 }
    };

    //this.test();
  }


  cleanup() {
    this.state.stages.world.entities.removeChildren();
    this.state.sprites.entities = GameInit.generateEntitySprites(
      this.state.dimensions[0],
      this.state.dimensions[1],
      this.gameState.entityLayer,
      this.gameState.entitySet
    );

    this.state.sprites.entities.map((sprite) => {
      this.state.stages.world.entities.addChild(sprite);
    });
  }

  generateEntitySprite(entityID) {
    // Sprite creator. This should be replaced with a real sprite management system at some point.
    let sprite = GameRender.generateEntitySprite(this.state.dimensions, entityID);
    let entitySprites = this.state.sprites.entities;
    let entityStage = this.state.stages.world.entities;

    entitySprites.push(sprite);
    entityStage.addChild(sprite);

    return sprite;
  }


  getRenderer() {
    return this.renderer.view;
  }


  test() {
    /*let sprite = new PIXI.Sprite.fromImage("/static/img/loxi.png");
    let [width, height] = this.state.dimensions;

    sprite.x = MathUtils.randomRange(0, width);
    sprite.y = MathUtils.randomRange(0, height);

    sprite.height = 150;
    sprite.width = 150;

    this.state.stages.testing.addChild(sprite);*/
  }


  loop() {
    // Check to see if we must cleanup prior to rendering a new dungeon.
    if (this.gameState.UI.waitingOnDungeonRequest === true) {

      // Is there a generated dungeon queued to replace this one?
      if (window.nextGameState !== undefined) {
        this.store.dispatch({
          'type': "SET_GAME_STATE",
          'state': window.nextGameState
        });

        window.nextGameState = undefined;

        this.cleanup();
      }
    }

    let player = this.gameState.entityLayer[0];

    if (this.state.gameStateChanged === true) {

      // Create a blob of commonly used data
      // to save ourselves some effort.
      let baseData = GameRender.getBaseData(
        player,
        this.gameState.tileSet,
        this.gameState.tileLayer,
        this.state.dimensions,
        this.gameState.mapHeight,
        this.gameState.mapWidth
      );

      // Send our to various stages and sprite
      // layers off to be mutated.

      // Render Tiles
      GameRender.renderTiles(
        baseData,
        this.gameState.tileSet,
        this.gameState.tileLayer,
        this.state.sprites.tiles
      );

      // Render Player, enemies, items, objects.
      GameRender.renderEntities(
        baseData,
        this.gameState.entityLayer,
        this.state.sprites.entities,
        this.generateEntitySprite.bind(this)
      );

      // Render the minimap.
      GameRender.renderMinimap(
        baseData,
        this.gameState.tileSet,
        this.gameState.tileLayer,
        this.state.sprites.HUD.miniMap
      );

      // Update our screen position.
      this.state.panOffset = getScreenOffset(
        player.location,
        this.gameState.mapHeight,
        this.gameState.mapWidth,
        this.state.dimensions[0],
        this.state.dimensions[1]
      );

      // We achieve panning by setting world position to the inverse of our offset.
      this.state.stages.world.primary.x = -(this.state.panOffset.x);
      this.state.stages.world.primary.y = -(this.state.panOffset.y);

      this.state.gameStateChanged = false;
    }

    // Render our player HUD
    GameRender.renderHUD(
      player,
      this.state.sprites.HUD
    );

    // Pass state along to the Engine for handling animations.
    this.engine.loop(this.state);

    this.renderer.render(this.state.stages.primary);
  }
}
