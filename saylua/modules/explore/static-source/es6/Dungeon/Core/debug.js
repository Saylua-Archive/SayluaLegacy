// debug -> Required by Reducers/DebugReducer
// --------------------------------------
// Useful functions for the debug reducer.

export function revealMap(tileLayer, entityLayer) {
  for (let tile of tileLayer) {
    tile.meta.seen = true;
  }

  for (let entity of entityLayer) {
    entity.meta.seen = true;
    entity.location.lastSeen = {
      'x': entity.location.x,
      'y': entity.location.y
    };
  }

  return [tileLayer, entityLayer];
}
