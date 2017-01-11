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
  tileLayer.map((row, y) => {
    row.map((col, x) => {
      nodeGraph[x] = nodeGraph[x] || [];

      let currentTile = col.tile;
      let tileType = tileSet[currentTile].type;
      let isObstruction = (OBSTRUCTIONS.indexOf(tileType) !== -1);

      if (isObstruction) {
        nodeGraph[x].push(0);
      } else {
        nodeGraph[x].push(1);
      }
    });
  });

  return nodeGraph;
}
