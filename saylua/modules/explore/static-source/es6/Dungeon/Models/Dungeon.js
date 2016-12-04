/*eslint no-console: ["off"]*/
import BaseModel from "./BaseModel";
import Reqwest from "reqwest";

// Dungeon -> Required by DungeonClient.
// --------------------------------------
// Describes the schema and location of all tiles and entities on the client.
// Optimize here first if performance becomes an issue in the future.

export default class Dungeon extends BaseModel {
  constructor() {
    super();

    this.state = {
      "initialized": false,
      "lock": false,
      "model": this.defaults()
    };
  }

  defaults() {
    // The Dungeon model is described by four things:
    // -----------------------------------------
    // - The working set of tiles.
    // - The working set of entities.
    // - Ordered instances of Tiles. (The actual map)
    // - Unordered instances of Entities.
    //
    // It is possible that in the near future,
    // tilesets and entity sets will be hidden from
    // the player and stored locally.

    return {
      "tileSet": [],
      "entitySet": [],
      "tileLayer": [],
      "entityLayer": []
    };
  }

  _debug_regenerate(bind) {
    if (bind === true) {
      return this._debug_regenerate.bind(this);
    } else {
      this.fetch({}, {"regenerate": true});
    }
  }

  _debug_reveal(bind) {
    if (bind === true) {
      return this._debug_reveal.bind(this);
    } else {
      this.fetch({}, {"reveal": true});
    }
  }

  fetch(mutation, debug) {
    mutation = mutation ? mutation : {};
    debug = debug ? debug : {};

    // Ensure that we don't end up with race conditions.
    if (this.state.lock === true) {
      return false;
    }

    this.state.lock = true;

    let promise = Reqwest({
      "url": '/api/explore/get/',
      "type": 'json',
      "method": 'post',
      "data": {
        "initial": !this.state.initialized,
        "mutation": JSON.stringify(mutation),
        "debug": JSON.stringify(debug)
      },
      "error": (error) => {
        console.log("Error syncing with Dungeon API.");
      },
      "success": (response) => {
        if (this.state.initialized === false) {
          this.state.model = response;
          this.state.initialized = true;
        } else {
          this.state.model = this.mergeDiff(response, debug);
        }
      }
    });

    promise.always((response) => {
      this.state.lock = false;
      if (this.state.initialized) {
        this.triggerUpdate();
      }
    });

    return promise;
  }

  get(attr) {
    // Reasons
    return this.state.model[attr];
  }

  mergeDiff(diff, debug) {
    if (debug.reveal !== undefined || debug.regenerate !== undefined) {
      return diff;
    }

    let newModel = this.state.model;

    // There's no real point in removing entity or tile schema,
    // We will assume any differences to sets are additions.
    newModel.entitySet.concat(diff.entitySet);
    newModel.tileSet.concat(diff.tileSet);

    // Full-replace changed entities. Rewrite this to only change
    // modified attributes, if performance becomes an issue.

    // -- Might be a good idea to consider indexing this.
    newModel.entityLayer = newModel.entityLayer.map((e, i, a) => {
      let changedEntity = diff.entityLayer.filter((_e) => _e.id === e.id)[0];
      return changedEntity ? changedEntity : e;
    });

    // Does not diff deeply, checks for changes and replaces the entire cell.
    // Unseen cells are represented as empty objects.
    diff.tileLayer.map((row, y , a) => {
      row.map((cell, x, a) => {
        if (Object.keys(cell).length !== 0) {
          newModel.tileLayer[y][x] = cell;
        } else {
          // Do we have this cell in memory already?
          if (Object.keys(this.state.model.tileLayer[y][x]).length > 0) {
            // Our cell is now hidden, but seen.
            newModel.tileLayer[y][x]['meta']['visible'] = false;
          }
        }
      });
    });

    return newModel;
  }

  mutate(mutation) {
    // For now, the only possible mutation is movement.
    // i.e. {"mutation": "move": "data": "up"}
    //
    // This is futureproofing in the event of things such as inventories, items, UI interactions, etc.
    // e.g. {"mutation": "use": "data": "<item-id>"},
    //      {"mutation": "equip": "data": "<item-id>"},
    //      {"mutation": "switch": "data": "<pet-id>"}

    this.fetch(mutation);
  }
}
