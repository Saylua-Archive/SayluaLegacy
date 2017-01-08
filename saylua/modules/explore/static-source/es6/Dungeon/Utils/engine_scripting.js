import * as MathUtils from "./math";


const ENABLED_SPECIAL_VARIABLES = [
  '$this',
  '$tileLayer',
  '$entityLayer',
  '$tiles',
  '$entities',
  '$entity_nearest',
  '$entity_nearest_@type',
  '__log'
  //$location
  //$location.screen
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
      console.log("Search pattern: " + pattern);

      // Construct pattern and search
      pattern = new RegExp(pattern, "gm");
      let results = payload.match(pattern);
      console.log(`Wildcard results: ${results}`);

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

    // Good.
    if (payload.indexOf(specialVariable) !== -1) {
      requires.push(specialVariable);
      return;
    }
  });

  // Translate required special arguments into function args
  let args = requires.map((requirement) => requirement.split('.')[0]).join(",");

  // Compile and store.
  console.log("Compiling: " + `window.__tfunc = function(${args}) { ${payload} }`);
  eval(`window.__tfunc = function(${args}) { ${payload} }`);

  window.scriptEngineFunctions[id]['requires'] = requires;
  window.scriptEngineFunctions[id]['function'] = window.__tfunc;

  delete window.__tfunc;
  return window.scriptEngineFunctions[id];
}


function resolveScript(scriptFunction, meta) {
  let args = [];

  // Necessary so that we can actually bind arguments dynamically to generated scripts.
  for (let requirement of scriptFunction.requires) {
    let result;
    let strippedRequirement = requirement.replace('$', '');
    let metaRequirements = Object.keys(meta);
    let metaContainsRequirement = (metaRequirements.indexOf(strippedRequirement) !== -1);

    // We will manually inject a few things ourselves, as the engine will not be able to provide an up-to-date result.
    if (metaContainsRequirement) {
      result = metaRequirements[strippedRequirement];
    } else {
      console.log(`Requesting ${requirement} on behalf of ${scriptFunction.id}`);
      result = resolveVariable(scriptFunction.id, requirement, meta);
      console.log(`Got back ${result}`);
    }

    args.push(result);
  }

  scriptFunction.function.apply(this, args);
}


export function resolveActions(actionType, actionLocation, tileSet, tileLayer, entitySet, entityLayer) {
  // What are we trying to find matching events for, here?
  let event = actionType.replace("HOOK_", "").toLowerCase();

  // Make sure that we are operating from copies.
  let newTileLayer = tileLayer.splice(0);
  let newEntityLayer = entityLayer.splice(0);

  if (event === 'enter') {
    let x = actionLocation.x;
    let y = actionLocation.y;

    // Entities first
    let matchingEntities = newEntityLayer.filter((entity) => {
      let isNotPlayer = (entity.parent !== '0x1000');
      let isSameLocation = ((entity.location.x == actionLocation.x) && (entity.location.y == actionLocation.y));

      return (isNotPlayer && isSameLocation);
    });

    for (let entity of matchingEntities) {
      console.log("We have just entered the same tile as an entity.");
      let parentEntity = entitySet[entity.parent];
      console.log(parentEntity);

      // First, we run the local instance's scripts, if possible.
      if (entity.events !== undefined) {
        if (entity.events[event] !== undefined) {
          console.log("We have a matching entity instance event!");
          let script = generateScript(entity.id, entity.events[event]);
          resolveScript(script, {
            'location': actionLocation,
            'tileSet': tileSet,
            'entitySet': entitySet,
            'tileLayer': newTileLayer,
            'entityLayer': newEntityLayer
          });
        }
      }// else { console.log('instance events.enter is undefined'); }

      // Then, we try the parent entity's scripts.
      if (parentEntity.events !== undefined) {
        if (parentEntity.events[event] !== undefined) {
          console.log("We have a matching entity type event!");
          let script = generateScript(parentEntity.id, parentEntity.events[event]);
          resolveScript(script, {
            'location': actionLocation,
            'tileSet': tileSet,
            'entitySet': entitySet,
            'tileLayer': newTileLayer,
            'entityLayer': newEntityLayer
          });
        }
      }// else { console.log('type events.enter is undefined'); }
    }
  }

  return [newEntityLayer, newTileLayer];
}

function resolveVariable(id, specialVariable, meta) {
  let splitVar = specialVariable.split('_');

  // A one time indexing on every layer update probably makes more sense than this nonsense.
  if (specialVariable === '$this') {
    // Search each group, in order of least numerous to most numerous.

    // Is there an entity type that matches?
    let matchingEntityType = meta.entitySet[id];
    if (matchingEntityType !== undefined) {
      return matchingEntityType;
    }

    // Is there a tile type that matches?
    let matchingTileType = meta.tileSet[id];
    if (matchingTileType !== undefined) {
      return matchingTileType;
    }

    // Is there an entity instance that matches?
    let matchingEntityInstance = meta.entityLayer.filter((entity) => entity.id === id);
    if (matchingEntityInstance.length > 0) {
      return matchingEntityInstance[0];
    }

    // Is there a tile instance that matches?
    let matchingTileInstance = meta.tileLayer.filter((tile) => tile.id === id);
    if (matchingTileInstance.length > 0) {
      return matchingTileInstance[0];
    }

    // wtf
    return "WE HAV EA PROBLEML SOMEONE SPLASE HLEP ME";
  }

  if (specialVariable === '$entity.nearest') {
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

  if (specialVariable === '__log') {
    // For now, we're just going to provide the traditional console.log
    return console.log;
  }
}
