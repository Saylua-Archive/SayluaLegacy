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

import SpriteManager from "./SpriteManager";
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

    // Initialize Pixi renderer
    this.renderer = PIXI.autoDetectRenderer(renderWidth, renderHeight, undefined, false, true);

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

    // Start our miniMap off SHOWN, SUCKA.
    stages.HUD.miniMap.visible = true;

    // Generate the various sprite layers necessary.
    let tileSprites = GameInit.generateTileSprites(
      this.gameState.mapHeight,
      this.gameState.mapWidth
    );

    let entitySprites = GameInit.generateEntitySprites(
      this.gameState.entityLayer
    );

    let HUDSprites = GameInit.generateHUDSprites({
      renderWidth,
      renderHeight,
      'mapHeight': this.gameState.mapHeight, // Total map height
      'mapWidth': this.gameState.mapWidth // Total map width
    });

    // Initialize and store the Entity Sprite Manager
    this.entityManager = new SpriteManager(store, stages.world.entities);
    this.entityManager.addSprite(entitySprites);

    // Initialize and store the Animation Engine
    this.engine = new Engine(store, this.entityManager);

    let sprites = {
      "tiles": tileSprites,
      "HUD": HUDSprites
    };

    // Final setup

    // -- Mouse Handler: Tile highlights, Master Hand cursor and debugger previews.
    let tileHoverHandler = MouseInteractions.tileHover(sprites.HUD.mouse, this);
    let tileClickHandler = MouseInteractions.tileClick(this);

    // -- Mouse Handler: Viewport panning
    let panDragStart = MouseInteractions.panDragStart(this);
    let panDragEnd = MouseInteractions.panDragEnd(this);
    let panDragMove = MouseInteractions.panDragMove(this);

    // -- Mouse Handler: Viewport Zooming
    MouseInteractions.viewportZoom('.dungeon-wrapper', this);


    // -- Bind our viewport panning handlers to the world container.
    stages.world.primary.interactive = true;
    stages.world.primary
      .on('pointerdown', panDragStart)
      .on('pointermove', panDragMove)
      .on('pointerup', panDragEnd)
      .on('pointerupoutside', panDragEnd);

    // -- Bind tile events, append tile sprites to tile stage
    sprites.tiles.map((sprite) => {
      // Bind mouse events
      sprite.interactive = true;
      sprite.buttonMode = true;

      sprite.on('pointerdown', tileClickHandler);
      sprite.on('pointerover', tileHoverHandler);

      // Append to the stage
      stages.world.tiles.addChild(sprite);
    });

    // -- Append minimap sprites to the HUD.miniMap stage.
    sprites.HUD.miniMap.map((sprite) => {
      stages.HUD.miniMap.addChild(sprite);
    });

    // -- Append health sprites to the HUD.playerStatus stage.
    sprites.HUD.playerStatus.map((sprite) => {
      stages.HUD.playerStatus.addChild(sprite);
    });

    // -- Append mouse sprites to the HUD.mouse stage.
    sprites.HUD.mouse.map((sprite) => {
      stages.HUD.mouse.addChild(sprite);
    });


    // Finally, we define a default state to hold all of this.
    this.state = {
      "dimensions": [renderHeight, renderWidth],
      "gameStateChanged": true,
      stages,
      sprites,
      "zoomLevel": 1,
      "panOffset": { "x": 0, "y": 0 },
      "currentlyDragging": false
    };
  }


  /******************************** META FUNCTIONS ***********************************/

  cleanup() {
    // Wipe and re-generate our entity sprites. Tile sprites are already reusable,
    // as all maps currently possess the same dimensions.
    this.entityManager.cleanup();
    this.state.stages.world.entities.removeChildren();

    let entitySprites = GameInit.generateEntitySprites(
      this.gameState.entityLayer
    );

    this.entityManager.addSprite(entitySprites);
    entitySprites.map(e => this.state.stages.world.entities.addChild(e));
  }


  regenerateDungeon() {
    // Is there a generated dungeon queued to replace this one?
    if (window.specialEventQueue.nextGameState !== undefined) {
      this.store.dispatch({
        'type': "SET_GAME_STATE",
        'state': window.specialEventQueue.nextGameState
      });

      window.specialEventQueue.nextGameState = undefined;

      this.cleanup();
    }
  }


  getRenderer() {
    return this.renderer.view;
  }


  test() {
    console.log("Hello! I am the test!");
  }


  /******************************** RENDERER SPECIFIC FUNCTIONS ***********************************/

  renderHUD() {
    let player = this.gameState.entityLayer[0];

    GameRender.renderHUD(
      player,
      this.state.sprites.HUD
    );
  }


  renderWorld() {
    let player = this.gameState.entityLayer[0];

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
      this.entityManager.children
    );

    // Render the minimap.
    GameRender.renderMinimap(
      baseData,
      this.gameState.tileSet,
      this.gameState.tileLayer,
      this.state.sprites.HUD.miniMap
    );
  }


  updateScreenPosition(options) {
    // Default to centering on the player's position
    options = options || {
      "type": "player",
      "location": this.gameState.entityLayer[0].location,
      "format": "grid",
      "center": true
    };

    // Zoom on the mouse's current position.
    if (options.type === "mouse") {
      options.location = this.renderer.plugins.interaction.mouse.global;
      options.format = "pixel";
      options.center = false;
    }

    this.state.panOffset = getScreenOffset(
      options,
      this.gameState.mapHeight,
      this.gameState.mapWidth,
      this.state.dimensions[0],
      this.state.dimensions[1],
      this.state.panOffset,
      this.state.zoomLevel
    );

    // We achieve panning by setting world position to the inverse of our offset.
    this.state.stages.world.primary.x = -(this.state.panOffset.x);
    this.state.stages.world.primary.y = -(this.state.panOffset.y);
  }


  loop() {
    // Check to see if we must cleanup prior to rendering a new dungeon.
    if (this.gameState.UI.waitingOnDungeonRequest === true) {
      this.regenerateDungeon();
    }

    // Update sprites if necessary
    if (window.specialEventQueue.summonEntity !== undefined) {
      let newEntity = window.specialEventQueue.summonEntity;
      let newSprite = this.entityManager.generateSprite(newEntity);

      this.entityManager.addSprite(newSprite);

      window.specialEventQueue.summonEntity = undefined;
    }

    // Re-render the world if necessary.
    if (this.state.gameStateChanged === true) {
      this.renderWorld();
      this.updateScreenPosition();

      this.state.gameStateChanged = false;
    }

    // Re-render the HUD every frame.
    this.renderHUD();

    // Pass state along to the Engine for handling animations.
    this.engine.loop(this.state);

    // Paint our current game state with Pixi.
    this.renderer.render(this.state.stages.primary);
  }
}
