// scripting -> Required by Reducers/GameReducer
// --------------------------------------
// The heart of Dungeons' game scripting.

import astar from "astar";

import * as MathUtils from "../Utils/math";
import * as EngineUtils from "../Utils/engine";

import { OBSTRUCTIONS } from "./logic";


const ENABLED_SPECIAL_VARIABLES = [
  '$this',
  '$tileLayer',
  '$entityLayer',
  '$tiles',
  '$player',
  '$entities',
  '$entity_nearest',
  '$entity_nearest_@type',
  '$location',
  '__distance',
  '__isObstacle',
  '__log',
  '__moveTo',
  '__rand',
  // Temporary
  '__debugMove',
  '__debugAttack'
];

const WORKERS_ENABLED = (window.Worker !== undefined);


function compileScript(id, payload) {
  // Initialize if necessary.
  window.scriptEngineFunctions = window.scriptEngineFunctions || {};
  window.scriptEngineFunctions[id] = window.scriptEngineFunctions[id] || {};

  // Prevent re-compiling, for speed reasons. May want to add a recompile flag later.
  if (window.scriptEngineFunctions[id]['function'] !== undefined) {
    return window.scriptEngineFunctions[id];
  }

  // Reasons.
  window.scriptEngineFunctions[id]['id'] = id;

  // Build a list of the special variables that a function requires.
  let requires = [];

  ENABLED_SPECIAL_VARIABLES.map((specialVariable) => {
    // Do we need to perform a wildcard regex?
    if (specialVariable.indexOf('@') !== -1) {

      // Escape search string
      let pattern = specialVariable
        .split('@')[0]
        .replace('$', '\\$');

      // Add a wildcard
      pattern = pattern + '[a-z]+';

      // Construct pattern and search
      pattern = new RegExp(pattern, "gm");
      let results = payload.match(pattern);

      if (results === null) {
        return;
      }

      // Add each unique result to the requirements.
      results.filter((e, i, a) => {
        return a.indexOf(e) === i;
      }).map((e) => {
        requires.push(e);
      });

      return;
    }

    // Good. We still have to do a normal regex though.
    let pattern = specialVariable.replace('$', '\\$');
    pattern = pattern + "[^_]";
    pattern = new RegExp(pattern, "gm");

    let results = payload.match(pattern);

    if (results !== null) {
      requires.push(specialVariable);
    }
  });

  // Translate required special arguments into function args
  let args = requires.map((requirement) => requirement.split('.')[0]).join(",");
  let functionString = `function(${args}) { ${payload} }`;
  // Compile and store.
  //console.log("Compiling: " + `window.__tfunc = function(${args}) { ${payload} }`);
  eval(`window.__tfunc = ${functionString};`);

  window.scriptEngineFunctions[id]['requires'] = requires;
  window.scriptEngineFunctions[id]['function'] = window.__tfunc;
  window.scriptEngineFunctions[id]['functionString'] = functionString;

  delete window.__tfunc;
  return window.scriptEngineFunctions[id];
}


function executeScript(scriptFunction, meta) {
  let args = [];
  let metaRequirements = Object.keys(meta);

  // Necessary so that we can actually bind arguments dynamically to generated scripts.
  for (let requirement of scriptFunction.requires) {
    let result;
    let strippedRequirement = requirement.replace('$', '');
    let metaContainsRequirement = (metaRequirements.indexOf(strippedRequirement) !== -1);

    // We will manually inject a few things ourselves, as the resolver will not be able to provide an accurate result.
    if (metaContainsRequirement) {
      result = meta[strippedRequirement];
    } else {
      //console.log(`Requesting ${requirement} on behalf of ${scriptFunction.id}`);
      result = resolveSpecialVariable(scriptFunction.id, requirement, meta);
      //console.log(`Got back: ${result}`); console.log(result);
    }

    args.push(result);
  }

  try {
    scriptFunction.function.apply(this, args);
    window.testA = scriptFunction.function.toString();
    window.testB = args;
  } catch(e) {
    console.log(`Script ${scriptFunction.id} failed: `);
    console.log(e);
  }
}


function resolveActorScripts(event, actor, data) {
  let script, parent;

  // Is it a child entity?
  if (actor.parent !== undefined) {
    parent = data.entitySet[actor.parent];
  }

  // Is it a child tile?
  if (actor.tile !== undefined) {
    parent = data.tileSet[actor.tile];
  }

  // First, we run the local instance's scripts, if possible.
  if (actor.events !== undefined) {
    if (actor.events[event] !== undefined) {
      script = compileScript(actor.id, actor.events[event]);
      executeScript(script, data);

      return 1;
    }
  }

  // Then, we try the parent entity's scripts.
  if (parent) {
    if (parent.events !== undefined) {
      if (parent.events[event] !== undefined) {
        script = compileScript(parent.id, parent.events[event]);
        executeScript(script, data);

        return 2;
      }
    }
  }

  // This thing had no scripts at all? Let's prevent it from being called again.
  actor.meta.noScripts = true;

  if (parent) {
    parent.meta = parent.meta || {};
    parent.meta.noScripts = true;
  }

  return false;
}


export function interpretGameEvents(data) {
  /*
    Example Usage:
    {
      'actionType': 'TRIGGER_EVENT_ENTER',
      'actionLocation', { 'x': 0, 'y': 0}
      'tileSet': <object:tileSet>,
      'tileLayer': <array:tileLayer>,
      'entitySet': <object:entitySet>,
      'entityLayer': <array:entityLayer>
    }
  */

  // What are we trying to find matching events for, here?
  let event = data.actionType.replace("TRIGGER_EVENT_", "").toLowerCase();

  // Assume we have been provided a copy, for performance reasons.
  let newTileLayer = data.tileLayer;
  let newEntityLayer = data.entityLayer;

  // The basic data that an event must pass, no matter what it is.
  // All event types must also provide a 'this', and 'location' arg.

  let baseData = {
    'tileSet': data.tileSet,
    'entitySet': data.entitySet,
    'tileLayer': data.tileLayer,
    'entityLayer': data.entityLayer,
    'nodeGraph': data.nodeGraph,
    'mapWidth': data.mapWidth
  };

  // Trigger events.enter on specified location.
  if (event === 'enter') {
    baseData.location = data.actionLocation;

    // Entities first
    newEntityLayer.filter((entity) => {
      // Filter to matching non-player, non-self entities.
      let isNotPlayer = (entity.parent !== '0x1000');
      let isSameLocation = ((entity.location.x == data.actionLocation.x) && (entity.location.y == data.actionLocation.y));
      let hasScripts = (entity.meta.noScripts !== true);

      return (isNotPlayer && isSameLocation && hasScripts);
    })
    .map((entity) => {
      baseData.this = entity;
      resolveActorScripts(event, entity, baseData);
    });

    // Now the tile.
    let linearPosition = ((data.actionLocation.y * data.mapWidth) + data.actionLocation.x);
    let tile = newTileLayer[linearPosition];
    baseData.this = tile;
    resolveActorScripts(event, tile, baseData);
  }

  // Process AI behaviors.
  if (event === 'timestep') {
    baseData.this = data.target;
    baseData.location = data.target.location;
    resolveActorScripts(event, data.target, baseData);
  }

  return [newEntityLayer, newTileLayer];
}

function resolveSpecialVariable(id, specialVariable, meta) {
  let splitVar = specialVariable.split('_');

  if (specialVariable === '$player') {
    return meta.entityLayer[0];
  }

  if (specialVariable === '$entity_nearest') {
    // Search every entity, stopping at any point if an entity other than itself is located in the same tile.
    // There are probably some approximation methods we could use here to speed this up,
    // but it is unlikely this will be used often enough to require them.
    let nearestEntity = meta.entityLayer[0];
    let nearestDistance = 99999; // This is one of those things that is never broken, until it is.

    for (let entity of meta.entityLayer) {
      if (entity.id !== id) {
        let isSameLocation = (
          (entity.location.x === meta.location.x) &&
          (entity.location.y === meta.location.y)
        );

        // Have we found a same-location entity? Stop the search and return.
        if (isSameLocation) {
          nearestEntity = entity;
          break;
        }

        let distance = MathUtils.distance(entity.location, meta.location);
        if (distance < nearestDistance) {
          nearestEntity = entity;
          nearestDistance = distance;
        }
      }
    }

    return nearestEntity;
  }

  // Hello yes it is me, Enterprise Java.
  let isNearestEntityTypeSearch = (
    (splitVar[0] === '$entity') &&
    (splitVar.indexOf('nearest') !== -1) &&
    (typeof(splitVar[2]) === 'string')
  );

  if (isNearestEntityTypeSearch) {
    // What type are we searching for?
    let searchType = splitVar[2];

    // Filter to the selected type, first.
    let matchingEntities = meta.entityLayer.filter((entity) => {
      return (
        (entity.id !== id) &&
        (meta.entitySet[entity.parent].type === searchType)
      );
    });

    let nearestEntity = matchingEntities[0];
    let nearestDistance = 99999; // This is one of those things that is never broken, until it is.

    for (let entity of matchingEntities) {
      let isSameLocation = (
        (entity.location.x === meta.location.x) &&
        (entity.location.y === meta.location.y)
      );

      // Have we found a same-location entity? Stop the search and return.
      if (isSameLocation) {
        nearestEntity = entity;
        break;
      }

      let distance = MathUtils.distance(entity.location, meta.location);
      if (distance < nearestDistance) {
        nearestEntity = entity;
        nearestDistance = distance;
      }
    }

    return nearestEntity;
  }

  if (specialVariable === '__debugAttack') {
    window.queuedAttacks = window.queuedAttacks || [];

    let debugAttack = (id, damage) => {
      window.queuedAttacks.push([id, damage]);
    };

    return debugAttack;
  }

  if (specialVariable === '__debugMove') {
    window.queuedMoves = window.queuedMoves || [];

    let debugMove = (nodeGraph) => (id, oldPosition, newPosition) => {
      // Add weight to our old location
      let oldNode = nodeGraph.grid[oldPosition.x][oldPosition.y];

      if (oldNode.priorWeight !== undefined) {
        oldNode.weight = oldNode.priorWeight;
      }

      // Unweight our new location
      let newNode = nodeGraph.grid[newPosition.x][newPosition.y];
      newNode.priorWeight = newNode.weight;

      let newWeight = Math.max(0, (newNode.weight - 1));
      newNode.weight = newWeight;

      // Log move event to a global queue used for animation.
      window.queuedMoves.push([id, oldPosition, newPosition]);
    };

    return debugMove(meta.nodeGraph);
  }

  if (specialVariable === '__distance') {
    return MathUtils.distance;
  }

  if (specialVariable === '__log') {
    return EngineUtils.log;
  }

  if (specialVariable === "__isObstacle") {
    let curry = (tileSet, tileLayer, mapWidth, obstructions) => (location) => {

      let linearPosition = (location.y * mapWidth) + location.x;
      let tileExists = (tileLayer[linearPosition] !== undefined);

      if (tileExists) {
        // There is a tile in this position. Is it the right one?
        let validTile = (
          tileLayer[linearPosition].location.x === location.x &&
          tileLayer[linearPosition].location.y === location.y
        );

        if (validTile) {
          let parentTileID = tileLayer[linearPosition].tile;
          let parentTileType = tileSet[parentTileID].type;
          return (obstructions.indexOf(parentTileType) !== -1);
        }
      }

      return true;
    };

    return curry(meta.tileSet, meta.tileLayer, meta.mapWidth, OBSTRUCTIONS);
  }

  if (specialVariable === '__moveTo') {
    let curry = (nodeGraph) => (data) => {
      let start, end;

      start = nodeGraph.grid[data.location.x][data.location.y];
      end = nodeGraph.grid[data.target.x][data.target.y];

      let result = astar.astar.search(nodeGraph, start, end, { 'heuristic': astar.astar.heuristics.diagonal });
      return result;
    };

    return curry(meta.nodeGraph);
  }

  if (specialVariable === '__rand') {
    return MathUtils.randomRange;
  }
}
