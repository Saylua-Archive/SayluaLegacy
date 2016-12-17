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

  fetch() {
    // Ensure that we don't end up with race conditions.
    if (this.state.initialized === true) {
      return false;
    }

    let promise = Reqwest({
      "url": '/explore/api/generate_dungeon',
      "type": 'json',
      "method": 'post',
      "error": (error) => {
        console.log("Error syncing with Dungeon API.");
      },
      "success": (response) => {
        this.state.model = response;
        this.state.initialized = true;
      }
    });

    promise.always((response) => {
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
}
