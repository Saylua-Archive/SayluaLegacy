import astar from "astar";
import cloneDeep from "lodash.clonedeep";
import * as MathUtils from "./math";
import * as EngineUtils from "./engine";


import { OBSTRUCTIONS } from "./game_helpers";


const ENABLED_SPECIAL_VARIABLES = [
  '$this',
  '$tileLayer',
  '$entityLayer',
  '$tiles',
  '$entities',
  '$entity_nearest',
  '$entity_nearest_@type',
  '$location',
  '__distance',
  '__isObstacle',
  '__log',
  '__moveTo',
  '__rand'
];


function generateScript(id, payload) {
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

  // Compile and store.
  //console.log("Compiling: " + `window.__tfunc = function(${args}) { ${payload} }`);
  eval(`window.__tfunc = function(${args}) { ${payload} }`);

  window.scriptEngineFunctions[id]['requires'] = requires;
  window.scriptEngineFunctions[id]['function'] = window.__tfunc;

  delete window.__tfunc;
  return window.scriptEngineFunctions[id];
}


function resolveScript(scriptFunction, meta) {
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
      result = resolveVariable(scriptFunction.id, requirement, meta);
      //console.log(`Got back: ${result}`); console.log(result);
    }

    args.push(result);
  }

  scriptFunction.function.apply(this, args);
}


export function resolveActions(data) {
  /*
    Example Usage:
    {
      'actionType': 'HOOK_ENTER',
      'actionLocation', { 'x': 0, 'y': 0}
      'tileSet': <object:tileSet>,
      'tileLayer': <array:tileLayer>,
      'entitySet': <object:entitySet>,
      'entityLayer': <array:entityLayer>
    }
  */

  // What are we trying to find matching events for, here?
  let event = data.actionType.replace("HOOK_", "").toLowerCase();

  // Make sure that we are operating from copies.
  let newTileLayer = data.tileLayer.slice();
  let newEntityLayer = data.entityLayer.slice();

  // Trigger entities / tiles at the players new location.
  if (event === 'enter') {

    // Entities first
    let matchingEntities = newEntityLayer.filter((entity) => {
      let isNotPlayer = (entity.parent !== '0x1000');
      let isSameLocation = ((entity.location.x == data.actionLocation.x) && (entity.location.y == data.actionLocation.y));

      return (isNotPlayer && isSameLocation);
    });

    for (let entity of matchingEntities) {
      //console.log("We have just entered the same tile as an entity.");
      let parentEntity = data.entitySet[entity.parent];
      //console.log(parentEntity);

      // First, we run the local instance's scripts, if possible.
      if (entity.events !== undefined) {
        if (entity.events[event] !== undefined) {
          //console.log("We have a matching entity instance event!");
          let script = generateScript(entity.id, entity.events[event]);
          resolveScript(script, {
            'this': entity,
            'location': data.actionLocation,
            'tileSet': data.tileSet,
            'entitySet': data.entitySet,
            'tileLayer': newTileLayer,
            'entityLayer': newEntityLayer,
            'nodeGraph': data.nodeGraph
          });
        }
      }// else { console.log('instance events.enter is undefined'); }

      // Then, we try the parent entity's scripts.
      if (parentEntity.events !== undefined) {
        if (parentEntity.events[event] !== undefined) {
          //console.log("We have a matching entity type event!");
          let script = generateScript(parentEntity.id, parentEntity.events[event]);
          resolveScript(script, {
            'this': entity,
            'location': data.actionLocation,
            'tileSet': data.tileSet,
            'entitySet': data.entitySet,
            'tileLayer': newTileLayer,
            'entityLayer': newEntityLayer,
            'nodeGraph': data.nodeGraph
          });
        }
      }// else { console.log('type events.enter is undefined'); }
    }
  }

  // Process AI behaviors.
  if (event === 'timestep') {
    let target = data.target;
    let isTile = (target.tile !== undefined);
    let isEntity = !isTile;

    if (isEntity) {
      let parentEntity = data.entitySet[target.parent];

      if (target.events !== undefined) {
        if (target.events[event] !== undefined) {
          let script = generateScript(target.id, target.events[event]);
          resolveScript(script, {
            'this': target,
            'location': target.location,
            'tileSet': data.tileSet,
            'entitySet': data.entitySet,
            'tileLayer': newTileLayer,
            'entityLayer': newEntityLayer,
            'nodeGraph': data.nodeGraph
          });
        }
      }

      if (parentEntity.events !== undefined) {
        if (parentEntity.events[event] !== undefined) {
          let script = generateScript(parentEntity.id, parentEntity.events[event]);
          resolveScript(script, {
            'this': target,
            'location': target.location,
            'tileSet': data.tileSet,
            'entitySet': data.entitySet,
            'tileLayer': newTileLayer,
            'entityLayer': newEntityLayer,
            'nodeGraph': data.nodeGraph
          });
        }
      }
    }
  }

  return [newEntityLayer, newTileLayer];
}

function resolveVariable(id, specialVariable, meta) {
  let splitVar = specialVariable.split('_');

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

  if (specialVariable === '__distance') {
    return MathUtils.distance;
  }

  if (specialVariable === '__log') {
    return EngineUtils.log;
  }

  if (specialVariable === "__isObstacle") {
    let curry = (tileSet, tileLayer, obstructions) => (location) => {
      if (tileLayer[location.y] !== undefined) {
        if (tileLayer[location.y][location.x] !== undefined) {
          let currentTile = tileLayer[location.y][location.x].tile;
          let tileType = tileSet[currentTile].type;

          return (obstructions.indexOf(tileType) !== -1);
        }
      }

      return true;
    };

    return curry(meta.tileSet, meta.tileLayer.slice(), OBSTRUCTIONS);
  }

  if (specialVariable === '__moveTo') {
    let curry = (nodeGraph) => (data) => {
      let start = nodeGraph.grid[data.location.x][data.location.y];
      let end = nodeGraph.grid[data.target.x][data.target.y];

      let result = astar.astar.search(nodeGraph, start, end, { 'heuristic': astar.astar.heuristics.diagonal });
      return result;
    };

    return curry(meta.nodeGraph);
  }

  if (specialVariable === '__rand') {
    return MathUtils.randomRange;
  }
}
