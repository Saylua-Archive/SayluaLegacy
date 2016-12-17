const obstructions = [
  'wall'
];

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
  goalTile = tileSet.filter((tile) => tile.id === goalCell.tile)[0];
  tileType = goalTile['type'];

  if (obstructions.indexOf(tileType) !== -1) {
    return player.location;
  }

  return [g_x, g_y];
}


export function renderMap(entititySet, entityLayer, tileSet, tileLayer) {
  let entityLookupTable = [];

  for (let entity of entityLayer) {
    let x = entity.location.x;
    let y = entity.location.y;

    entityLookupTable[y] = entityLookupTable[y] || [];
    entityLookupTable[y][x] = entityLookupTable[y][x] || [];

    entityLookupTable[y][x].push(entity);
  }
}
