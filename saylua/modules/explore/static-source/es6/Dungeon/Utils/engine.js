import { OBSTRUCTIONS } from "./game_helpers";


export function log(message) {
  function padZeroes(number, width=2) {
    width -= number.toString().length;
    if (width > 0) {
      return new Array( width + (/\./.test( number ) ? 2 : 1) ).join( '0' ) + number;
    }
    return number + ""; // always return a string
  }

  // Create global log queue if necessary.
  // This logQueue is automatically consumed by our GameReducer when the state is updated.
  window.logQueue = window.logQueue || [];

  let now = new Date();
  let timestamp = `${padZeroes(now.getUTCHours())}:${padZeroes(now.getUTCMinutes())}:${padZeroes(now.getUTCSeconds())}`;
  let output = `${timestamp} - ${message}`;

  console.log(`Logging: ${output}`);
  window.logQueue.push(output);
  return output;
}

export function generateNodeGraph(tileSet, tileLayer) {
  let nodeGraph = [];

  // Our A* implementation uses [x][y] grids, so we must convert from our [y][x] grids.
  // Weight based on whether or not they are obstructions.
  for (let tile of tileLayer) {
    nodeGraph[tile.location.x] = nodeGraph[tile.location.x] || [];

    let parentTileType = tileSet[tile.tile].type;
    let isObstruction = (OBSTRUCTIONS.indexOf(parentTileType) !== -1);

    if (isObstruction) {
      nodeGraph[tile.location.x].push(0);
    } else {
      nodeGraph[tile.location.x].push(1);
    }
  }

  return nodeGraph;
}

export function normalizeTileLayer(tileLayer) {
  let mapHeight = tileLayer.length;
  let mapWidth = tileLayer[0].length;
  let normalizedTileLayer = [];

  for (let y = 0; y < mapHeight; y++) {
    for (let x = 0; x < mapWidth; x++) {
      let tile = tileLayer[y][x];

      tile.location = { x, y };
      normalizedTileLayer.push(tile);
    }
  }

  return [mapHeight, mapWidth, normalizedTileLayer];
}
