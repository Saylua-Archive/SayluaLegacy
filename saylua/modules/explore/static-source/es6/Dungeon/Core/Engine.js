// Engine -> Required by Components/GameRenderer
// --------------------------------------
// King of animations. Handles displaying the output of any
// changes in state that need to be animated.
//
// Would be called AnimationEngine if animation
// was the only thing it did.

// This entire class will be rewritten with the advent of animations.
// Very temporary code.

export default class Engine {
  constructor(store) {
    // Store store
    this.store = store;

    // Store store store
    this.gameState = this.store.getState();

    // Store store store store.
    // This will be triggered any time the store state changes.
    this.unsubscribe = this.store.subscribe(() => {
      this.gameState = store.getState();

      if (this.gameState.UI.canMove === true) {
        // Prevent the player from moving if animations must be processed.
        if ((window.queue.move.length) !== 0 || (window.queue.attack.length !== 0)) {
          this.store.dispatch({
            'type': "TOGGLE_MOVEMENT"
          });
        }
      }
    });

    this.state = {
      'animating': false
    };
  }

  loop(data) {
    // Are we currently generating a new dungeon?
    if (this.gameState.UI.waitingOnDungeonRequest === true) {
      if (this.gameState.UI.canMove === true) {
        this.store.dispatch({
          'type': "TOGGLE_MOVEMENT"
        });
      }
    }

    // Are we in the middle of animation?
    else if (this.gameState.UI.canMove === false) {

      // Are our animations complete?
      if ((window.queue.move.length === 0) && (window.queue.attack.length === 0) && (this.state.animating === false)) {
        // Enable movement where there are no queued animations.
        this.store.dispatch({
          'type': "TOGGLE_MOVEMENT"
        });
      }

      // We should be animating if we're not moving.
      else if (this.state.animating === false) {
        this.state.animating = true;
        // Animation code would normally go here.
        // We're going to resolve attacks and movement instantly for now.

        // Process movement animations
        for (let i = 0; i < window.queue.move.length; i++) {
          window.queue.move.pop();
        }

        // Process attack animations, apply attack damage.
        for (let i = 0; i < window.queue.attack.length; i++) {
          let attack = window.queue.attack.pop();
          let [attackerID, damage] = attack;

          this.store.dispatch({
            'type': "DAMAGE_PLAYER",
            'damage': damage
          });
        }

        this.state.animating = false;
      }
    }

    return;
  }
}
