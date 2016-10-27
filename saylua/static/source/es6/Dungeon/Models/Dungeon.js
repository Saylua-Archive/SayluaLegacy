import Reqwest from "reqwest";

// Dungeon -> Required by DungeonClient.
// --------------------------------------
// Describes the schema and location of all tiles and entities on the client.
// Optimize here first if performance becomes an issue in the future.

export default class Dungeon {
  constructor() {
    this.state = {
      "component": undefined,
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
    }
  }

  bindComponent(component) {
    // Slight amount of magic necessary in order to make sure
    // that when this model updates, our Component will also update.
    //
    // Our model will not appear to have updated if we only change it's attributes.
    // Therefore, we will component.setState() when a change is made.

    this.state.component = component;
    this.state.component.setState({
      "triggerUpdate": false
    });
  }

  fetch(action) {
    let mutation = action ? action : {};

    // Ensure that we don't end up with race conditions.
    if (this.state.lock === true) {
      return false;
    }

    let promise = Reqwest({
      "url": '/api/explore/get/',
      "type": 'json',
      "method": 'post',
      "data": {
        "initial": !this.state.initialized,
        "mutation": mutation
      },
      "error": (error) => {
        console.log("Error syncing with Dungeon API.");
      },
      "success": (response) => {
        if (this.state.initialized === false) {
          this.state.model = response;
          this.state.initialized = true;
        } else {
          this.state.model = this.mergeDiff(response);
        }
      }
    });

    promise.always((response) => {
      this.state.lock = false;
      if (this.state.initialized && this.state.component !== undefined) {
        this.state.component.setState({
          "triggerUpdate": !this.state.component.triggerUpdate
        });
      }
    });

    return promise;
  }

  mergeDiff(diff) {
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

    // Diff the actual tile map without micro-managing performance
    // by replacing any changed rows, rather than going cell by cell.
    //
    // Unchanged rows are represented as 'undefined'.
    diff.tileLayer.map((e, i , a) => {
      if (e !== undefined) {
        newModel.tileLayer[i] = e;
      }
    });

    return newModel;
  }

  mutate(action) {
    // For now, the only possible action is movement.
    // i.e. {"move": "up"}
    //
    // This is futureproofing in the event of things such as inventories, items, UI interactions, etc.
    // e.g. {"use": "<item-id>"}, {"equip": "<item-id>"}, {"switch": "<pet-id>"}

    this.state.lock = true;
    this.fetch(action);
  }
}