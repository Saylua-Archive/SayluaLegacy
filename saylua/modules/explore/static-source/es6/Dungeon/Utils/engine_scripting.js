const ENABLED_SPECIAL_VARIABLES = [
  '$this',
  //$tile
  //$entities
  //$location
  //$location.screen
  '__log'
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
    if (payload.indexOf(specialVariable) !== -1) {
      requires.push(specialVariable);
    }
  });

  // Translate required special arguments into function args
  let args = requires.join(",");

  // Compile and store.
  console.log("Compiling: " + `window.__tfunc = function(${args}) { ${payload} }`);
  eval(`window.__tfunc = function(${args}) { ${payload} }`);

  window.scriptEngineFunctions[id]['requires'] = requires;
  window.scriptEngineFunctions[id]['function'] = window.__tfunc;

  delete window.__tfunc;
  return window.scriptEngineFunctions[id];
}


function resolveScript(scriptFunction) {
  let args = [];

  // Necessary so that we can actually bind arguments dynamically to generated scripts.
  for (let requirement of scriptFunction.requires) {
    console.log(`Requesting ${requirement} on behalf of ${scriptFunction.id}`);
    let result = window.engineRequest(scriptFunction.id, requirement);
    console.log(`Got back ${result}`);
    args.push(result);
  }

  scriptFunction.function.apply(this, args);
}


export function resolveActions(actionType, actionLocation, tileSet, tileLayer, entitySet, entityLayer) {
  let event = actionType.replace("HOOK_", "").toLowerCase();

  if (event === 'enter') {
    let x = actionLocation.x;
    let y = actionLocation.y;

    // Entities first
    let matchingEntities = entityLayer.filter((entity) => {
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
          resolveScript(script);
        }
      } else { console.log('instance events.enter is undefined'); }

      // Then, we try the parent tile's scripts.
      if (parentEntity.events !== undefined) {
        if (parentEntity.events[event] !== undefined) {
          console.log("We have a matching entity type event!");
          let script = generateScript(parentEntity.id, parentEntity.events[event]);
          resolveScript(script);
        }
      } else { console.log('type events.enter is undefined'); }
    }
  }

  // We will do nothing, for now, and return them as-is.
  return [entityLayer, tileLayer];
}
