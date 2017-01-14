var player = $entity_nearest_player;
var self = $this;

var playerNearby = (__distance(player.location, self.location) < 6);

// Moves towards the player when very close.
if (playerNearby) {
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
      self.location.x = newLocation[0].x;
      self.location.y = newLocation[0].y;
    }
  }

  self.meta.chaseDistance = self.meta.chaseDistance + 1;

} else {
  //__log(`${self.id} - Moving randomly.`);
  // Move randomly otherwise.
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
