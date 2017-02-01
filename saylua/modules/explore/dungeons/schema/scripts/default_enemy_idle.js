var player = $player;
var self = $this;

var playerDistance = __distance(player.location, self.location);
var withinAttackDistance = (playerDistance < 2);
var playerNearby = (playerDistance < 6);


// Moves towards the player when close.
if ((playerNearby === true) && (withinAttackDistance === false)) {
  // Increment counter
  self.meta.chaseDistance = self.meta.chaseDistance || 0;

  // Clear the path and counter we use when idly roaming.
  self.meta.roamProgress = 0;
  self.meta.roamDistance = 0;
  self.meta.roamPath = [];

  // Returns an array of nodes to reach the player.
  // We only need the first one.
  if (self.meta.chaseDistance % 2 == 0) {
    var newLocation = __moveTo({
      'location': self.location,
      'target': player.location
    });
    //__log(`${self.id} - Moving to player`);


    if (newLocation[0] !== undefined) {
      // We will set the location instantly so that it registers as an obstacle
      // for other entities when pathing, but then enter a queue to be animated.
      var oldPosition = { 'x': self.location.x, 'y': self.location.y };

      self.location.x = newLocation[0].x;
      self.location.y = newLocation[0].y;

      // This will weight the old location, and unweight the new location, in addition
      // to adding it to an animation queue.
      __debugMove($this.id, oldPosition, self.location);
    }
  }

  self.meta.chaseDistance = self.meta.chaseDistance + 1;

}

// Attack the player when VERY close.
else if ((playerNearby === true) && (withinAttackDistance === true)) {
  // Clear the path and counter we use when idly roaming.
  self.meta.roamProgress = 0;
  self.meta.roamDistance = 0;
  self.meta.roamPath = [];

  var damage = __rand(4, 7);
  __debugAttack($this.id, damage);
}

// Roam around otherwise.
else {
  //__log(`${self.id} - Moving randomly.`);
  self.meta.chaseDistance = 0;

  // Initialize roam path.
  self.meta.roamProgress = self.meta.roamProgress || 0;
  self.meta.roamDistance = self.meta.roamDistance || [];
  self.meta.roamPath = self.meta.roamPath || [];

  // Establish a new roam path if we are out of nodes to navigate.
  if ((self.meta.roamProgress + 1) > (self.meta.roamPath.length - 1)) {

    // Reset path progress
    self.meta.roamProgress = 0;
    self.meta.roamDistance = 0;

    // Find a non-obstacle location.
    var isObstacle = true;
    var targetLocation;

    while (isObstacle) {
      targetLocation = {
        'x': self.location.x - __rand(-10, 10),
        'y': self.location.y - __rand(-10, 10)
      };

      if (!__isObstacle(targetLocation)) {
        //__log(`${self.id} - Trying new distance.`);
        if (__distance(self.location, targetLocation) > 2) {
          isObstacle = false;
        }
      }
    }

    self.meta.targetLocation = targetLocation;

    self.meta.roamPath = __moveTo({
      'location': self.location,
      'target': targetLocation
    });
  }

  var newLocation = self.meta.roamPath[self.meta.roamProgress];
  self.meta.roamDistance = self.meta.roamDistance + 0.7;
  self.meta.roamProgress = Math.floor(self.meta.roamDistance);

  if (newLocation !== undefined) {
    self.location.x = newLocation.x;
    self.location.y = newLocation.y;
  }
}
