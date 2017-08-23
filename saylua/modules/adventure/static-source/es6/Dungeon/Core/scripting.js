// scripting -> Required by Reducers/GameReducer
// --------------------------------------
// The heart of Dungeons' game scripting.

import * as MathUtils from "../Utils/math";
import * as EngineUtils from "../Utils/engine";

import { OBSTRUCTIONS } from "./logic";


const ENABLED_SPECIAL_VARIABLES = [
  '$entity_nearest',
  '$entity_nearest_@type',
  '$entityLayer',
  '$entitySet',
  '$location',
  '$player',
  '$this',
  '$tileLayer',
  '$tileSet',
  '__attack',
  '__distance',
  '__isObstacle',
  '__log',
  '__move',
  '__pathTo',
  '__queueEvent',
  '__rand'
];

//const WORKERS_ENABLED = (window.Worker !== undefined);


export function compileScript(id, payload, event, recompile=false) {
  // Initialize if necessary.
  window.scriptEngineFunctions = window.scriptEngineFunctions || {};
  window.scriptEngineFunctions[id] = window.scriptEngineFunctions[id] || {};
  window.scriptEngineFunctions[id][event] = window.scriptEngineFunctions[id][event] || {};

  // Prevent re-compiling, for speed reasons.
  if (window.scriptEngineFunctions[id][event]['function'] !== undefined) {
    if (recompile === false) {
      return window.scriptEngineFunctions[id][event];
    }
  }

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

  window.scriptEngineFunctions[id][event]['requires'] = requires;
  window.scriptEngineFunctions[id][event]['function'] = window.__tfunc;
  window.scriptEngineFunctions[id][event]['function'].__owner__ = id;
  window.scriptEngineFunctions[id][event]['function'].__event__ = event;
  window.scriptEngineFunctions[id][event]['payload'] = payload;
  //window.scriptEngineFunctions[id][event]['functionString'] = functionString;

  delete window.__tfunc;
  return window.scriptEngineFunctions[id][event];
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
  } catch(e) {
    console.log(`Script ${scriptFunction.__owner__}.${scriptFunction.__event__} failed: `); // eslint-disable-line no-console
    console.log(e); // eslint-disable-line no-console
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
      script = compileScript(actor.id, actor.events[event], event);
      executeScript(script, data);

      return 1;
    }
  }

  // Then, we try the parent entity's scripts.
  if (parent) {
    if (parent.events !== undefined) {
      if (parent.events[event] !== undefined) {
        script = compileScript(parent.id, parent.events[event], event);
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
      'actionType': 'onEnter',
      'actionLocation', { 'x': 0, 'y': 0}
      'tileSet': <object:tileSet>,
      'tileLayer': <array:tileLayer>,
      'entitySet': <object:entitySet>,
      'entityLayer': <array:entityLayer>
    }
  */

  // What are we trying to find matching events for, here?
  let event = data.actionType;

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
  if (event === 'onEnter') {
    baseData.location = data.actionLocation;

    // Entities first
    newEntityLayer.filter((entity) => {
      // Filter to matching non-player, non-self entities.
      let isNotPlayer = (entity.parent !== '0x1000');
      let isSameLocation = ((entity.location.x == data.actionLocation.x) && (entity.location.y == data.actionLocation.y));
      let hasScripts = (entity.meta.noScripts !== true);
      let isAlive = (entity.meta.dead !== true);

      return (isNotPlayer && isSameLocation && hasScripts && isAlive);
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
  if (event === 'onIdle') {
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

  if (specialVariable === '__attack') {
    let actorAttack = (id, args={}) => {
      window.queue['actorAttack'].push([id, args]);
    };

    return actorAttack;
  }

  if (specialVariable === '__move') {
    let move = (nodeGraph, entityLayer, mapWidth) => (id, oldPosition, newPosition) => {
      const graph = nodeGraph.graphs[0];
      const cost = nodeGraph.options.cost;
      const lineate = (x, y) => (x + (y * mapWidth));
      const potentialNeighbors = (location) => {
        let o_x = location.x;
        let o_y = location.y;

        return [
          [o_x-1, o_y],   // Cardinal Left
          [o_x+1, o_y],   // Cardinal Right
          [o_x, o_y-1],   // Cardinal Up
          [o_x, o_y+1],   // Cardinal Down
          [o_x-1, o_y-1], // Diagonal Upper-Left
          [o_x-1, o_y+1], // Diagonal Lower-Left
          [o_x+1, o_y-1], // Diagonal Upper-Right
          [o_x+1, o_y+1]  // Diagonal Lower-Right
        ];
      };

      // Decrease the cost of our old location
      let oldNode = graph.node({ 'x': oldPosition.x, 'y': oldPosition.y }, true);
      oldNode.cost = oldNode.priorCost;

      // Occlude our new location
      let newNode = graph.node({ 'x': newPosition.x, 'y': newPosition.y }, true);
      newNode.priorCost = newNode.cost;
      newNode.cost = 0;

      // Forge / update / remove edge connections as necessary in our old location
      potentialNeighbors(oldPosition)
        .map(n => graph.nodes.get(lineate(n[0], n[1])))
        .filter(n => n)
        .map(neighbor =>
          graph.edge(oldNode, neighbor, cost(oldNode, neighbor), cost(neighbor, oldNode))
        );

      // Forge / update / remove edge connections at our new location
      potentialNeighbors(newPosition)
        .map(n => graph.nodes.get(lineate(n[0], n[1])))
        .filter(n => n)
        .map(neighbor =>
          graph.edge(newNode, neighbor, cost(newNode, neighbor), cost(neighbor, newNode))
        );

      // Mark our actor as 'animated'.
      let matchingEntity = entityLayer.filter((entity) => entity.id === id)[0];
      matchingEntity.meta.animated = true;

      // Log move event to a global queue used for animation.
      window.queue['actorMove'].push([id, { oldPosition, newPosition }]);
    };

    return move(meta.nodeGraph, meta.entityLayer, meta.mapWidth);
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

  if (specialVariable === '__pathTo') {
    let curry = (nodeGraph) => (data) => {
      let result = nodeGraph.path(data.location, data.target);

      if (result.length !== 0) {
        result.shift();
      }

      return result;
    };

    return curry(meta.nodeGraph);
  }

  if (specialVariable === '__queueEvent') {
    let queueEvent = (id, args={}, blocking=false) => {
      window.queue['actorEvent'].push([id, { args, blocking }]);
    };

    return queueEvent;
  }

  if (specialVariable === '__rand') {
    return MathUtils.randomRange;
  }
}
