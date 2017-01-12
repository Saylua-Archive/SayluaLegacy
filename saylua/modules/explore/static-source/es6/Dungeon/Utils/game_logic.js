import { OBSTRUCTIONS } from "./game_helpers";
import { resolveActions } from "./engine_scripting";

export function translatePlayerLocation(player, tileLayer, tileSet, direction) {
  let p_x, p_y, g_x, g_y, goalCell, goalTile, tileType;

  p_x = player.location.x;
  p_y = player.location.y;

  g_x = p_x;
  g_y = p_y;

  switch(direction) {
    case 'up':
      g_y = p_y - 1;
      break;
    case 'down':
      g_y = p_y + 1;
      break;
    case 'left':
      g_x = p_x - 1;
      break;
    case 'right':
      g_x = p_x + 1;
      break;
  }

  // Determine if we can visit this tile, theoretically.
  try {
    goalCell = tileLayer[g_y][g_x];
  } catch (e) {
    return player.location;
  }

  if (goalCell === undefined) {
    return player.location;
  }

  // Determine if we can go there, physically.
  goalTile = tileSet[goalCell.tile];
  tileType = goalTile['type'];

  if (OBSTRUCTIONS.indexOf(tileType) !== -1) {
    return player.location;
  }

  return { "x": g_x, "y": g_y };
}


export function processAI(tileSet, tileLayer, entitySet, entityLayer, nodeGraph) {
  let referenceEntityLayer = entityLayer;
  let newEntityLayer = entityLayer.slice();
  let newTileLayer = tileLayer.slice();

  var t0 = performance.now();
  // Note that this operates from a copy.
  for (let entity of referenceEntityLayer) {

    // Does this entity still exist?
    // Entities have to determine whether or not they still exist due to cross-interactions.
    let matchingEntity = newEntityLayer.filter((_entity) => _entity.id == entity.id);

    if (matchingEntity.length > 0) {
      matchingEntity = matchingEntity[0];

      [newEntityLayer, newTileLayer] = resolveActions({
        'actionType': 'HOOK_TIMESTEP',
        'target': matchingEntity,
        'tileSet': tileSet,
        'tileLayer': newTileLayer,
        'entitySet': entitySet,
        'entityLayer': newEntityLayer,
        'nodeGraph': nodeGraph
      });
    }
  }

  var t1 = performance.now();
  console.log("Process AI entities took " + (t1 - t0) + " milliseconds.");

  let ddd = 0;
  for (let row of newTileLayer) {
    for (let tile of row) {
      if (ddd === 0) {
        t0 = performance.now();
      }
      [newEntityLayer, newTileLayer] = resolveActions({
        'actionType': 'HOOK_TIMESTEP',
        'target': tile,
        'tileSet': tileSet,
        'tileLayer': newTileLayer,
        'entitySet': entitySet,
        'entityLayer': newEntityLayer
      });

      if (ddd === 0) {
        t1 = performance.now();
        console.log("Process AI 1x tile took " + (t1 - t0) + " milliseconds.");
      }

      ddd = 1;
    }
  }

  return [newEntityLayer, newTileLayer];
}
