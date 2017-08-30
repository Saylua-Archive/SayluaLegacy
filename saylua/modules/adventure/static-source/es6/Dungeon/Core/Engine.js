// Engine -> Required by Components/GameRenderer
// --------------------------------------
// King of animations. Handles displaying the output of any
// changes in state that need to be animated.
//
// Would be called AnimationEngine if animation
// was the only thing it did.
//
// Also provisionally responsible for handling map
// reloads / game resets.
import { TILE_SIZE } from "./GameRenderer";
import { easeInOutExpo, easeInOutBack } from "../Utils/math";


export default class Engine {
  constructor(store, entityManager) {
    // Store store
    this.store = store;

    // Store store store
    this.gameState = this.store.getState();

    // Store store store store.
    // This will be triggered any time the store state changes.
    this.unsubscribe = this.store.subscribe(() => {
      this.gameState = store.getState();
    });

    // Store the Entity Sprite Manager
    this.entityManager = entityManager;

    this.state = {
      'animating': false,
      'temporaryRunningAnimationsList': [], // FIXME: Intentionally given obnoxious name. Refactor ASAP.
      'waitingForStoreSync': false
    };
  }


  createAnimation(type, actorID, args) {
    let animationData = {
      'expired': false,
      'timestamp': new Date()
    };

    this.state.temporaryRunningAnimationsList.push([type, animationData, actorID, args]);
  }


  loop(data) {
    // Disable movement if a dungeon is being regenerated.
    if (this.gameState.UI.waitingOnDungeonRequest === true) {
      if (this.gameState.UI.canMove === true) {
        this.store.dispatch({
          'type': "DISABLE_MOVEMENT"
        });
      }
    }


    // Should we be animating movements?
    if (this.state.animating === false && window.queue.actorMove.length > 0) {
      let [actorID, args] = window.queue.actorMove.shift();

      // Disable movement, halt further animations.
      this.state.animating = true;

      if (this.gameState.UI.canMove === true) {
        this.store.dispatch({
          'type': "DISABLE_MOVEMENT"
        });
      }

      this.createAnimation('actorMove', actorID, args);
    }


    // Should we be animating attack animations?
    // We only do this if all movement animations are complete.
    if (this.state.animating === false && window.queue.actorMove.length === 0 && window.queue.actorAttack.length > 0) {
      let [actorID, args] = window.queue.actorAttack.shift();

      // Disable movement, halt further animations, dispatch damage.
      /*this.state.animating = true;
      if (this.gameState.UI.canMove === true) {
        this.store.dispatch({
          'type': "DISABLE_MOVEMENT"
        });
      }
      this.store.dispatch({
        'type': "DAMAGE_PLAYER",
        'damage': damage
      });

      this.createAnimation('actorAttack', actorID, args);*/
    }


    // Any running animations should be processed.
    const now = new Date();
    const temporaryAnimationDuration = 300; // FIXME: Replace ASAP.

    const TILE_HEIGHT = TILE_SIZE;
    const TILE_WIDTH = TILE_SIZE;

    const VERTICAL_OFFSET = TILE_HEIGHT * 0.1;
    const HORIZONTAL_OFFSET = TILE_WIDTH * 0.1;

    this.state.temporaryRunningAnimationsList = this.state.temporaryRunningAnimationsList.filter(
      animation => !animation[1].expired
    );

    if (this.state.temporaryRunningAnimationsList.length === 0) {
      this.state.animating = false;
    }

    for (let animation of this.state.temporaryRunningAnimationsList) {
      let [type, data, actorID, args] = animation;

      if (type === "actorMove") {
        let timeElapsed = now - data.timestamp;
        let sprite = this.entityManager.getSprite(actorID);

        // Invisible sprites should not be animated.
        data.expired = (sprite.visible === false) ? true : (timeElapsed > temporaryAnimationDuration);

        // Calculate our goal coordinates.
        if (data.difference === undefined) {
          // Store the original sprite position as a reference
          data.spriteOrigin = {
            'x': sprite.x,
            'y': sprite.y,
            'height': sprite.height,
            'width': sprite.width
          };

          // Get our grid coords
          let oldPosition = args.oldPosition;
          let newPosition = args.newPosition;

          // Calculate grid difference
          let differenceX = newPosition.x - oldPosition.x;
          let differenceY = newPosition.y - oldPosition.y;

          // Translate grid difference into real pixels
          differenceX = differenceX * TILE_WIDTH;
          differenceY = differenceY * TILE_WIDTH;

          // Store the difference for positioning.
          data.difference = {
            'x': differenceX,
            'y': differenceY
          };

          // Make sprite brighter.
          sprite.blendMode = PIXI.BLEND_MODES.SCREEN;

          // Update entity location preemptively.
          let entity = this.entityManager.getEntity(actorID);
          entity.location.x = newPosition.x;
          entity.location.y = newPosition.y;
        }

        // Use goal coordinates to set sprite position.
        if (data.expired === false) {
          let percentageComplete = timeElapsed / temporaryAnimationDuration;

          let adjustedPercentageX = easeInOutExpo(percentageComplete);
          let adjustedPercentageY = easeInOutBack(percentageComplete);

          let currentPosition = {
            'x': (data.spriteOrigin.x + (data.difference.x * adjustedPercentageX)),
            'y': (data.spriteOrigin.y + (data.difference.y * adjustedPercentageY))
          };

          sprite.x = currentPosition.x;
          sprite.y = currentPosition.y;
          sprite.height = (data.spriteOrigin.height - 10) + (10 * adjustedPercentageY);
          sprite.width = (data.spriteOrigin.height + 5) - (5 * adjustedPercentageX);
        } else {
          // Return sprite to normal brightness.
          sprite.blendMode = PIXI.BLEND_MODES.NORMAL;

          // Expired entities should be snapped to their final position and original dimensions.
          sprite.x = Math.round((args.newPosition.x * TILE_WIDTH) + HORIZONTAL_OFFSET);
          sprite.y = Math.round((args.newPosition.y * TILE_HEIGHT) + VERTICAL_OFFSET);
          sprite.height = data.spriteOrigin.height;
          sprite.width = data.spriteOrigin.width;
        }
      }
    }


    // Do we need to re-enable movement?
    if (this.gameState.UI.canMove === false && this.state.animating === false) {
      if ((window.queue.actorMove.length === 0) && (window.queue.actorAttack.length === 0)) {
        // Enable movement where there are no queued animations.
        this.store.dispatch({
          'type': "ENABLE_MOVEMENT"
        });
      }
    }

    return;
  }
}
