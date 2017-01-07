export default class Engine {
  constructor(store) {
    // Store store
    this.store = store.getState();

    // Store store store store.
    // This will be triggered any time the store state changes.
    this.unsubscribe = store.subscribe(() => {
      this.store = store.getState();
    });

    window.engineRequest = this.engineRequest.bind(this);
  }

  engineRequest(id, specialVariable) {
    if (specialVariable === '$this') {
      // Search each group, in order of least numerous to most numerous.

      // Is there an entity type that matches?
      let matchingEntityType = this.store.entitySet[id];
      if (matchingEntityType !== undefined) {
        return matchingEntityType;
      }

      // Is there a tile type that matches?
      let matchingTileType = this.store.tileSet[id];
      if (matchingTileType !== undefined) {
        return matchingTileType;
      }

      // Is there an entity instance that matches?
      let matchingEntityInstance = this.store.entityLayer.filter((entity) => entity.id === id);
      if (matchingEntityInstance.length > 0) {
        return matchingEntityInstance[0];
      }

      // Is there a tile instance that matches?
      let matchingTileInstance = this.store.tileLayer.filter((tile) => tile.id === id);
      if (matchingTileInstance.length > 0) {
        return matchingTileInstance[0];
      }

      // wtf
      return "WE HAV EA PROBLEML SOMEONE SPLASE HLEP ME";
    }

    if (specialVariable === '__log') {
      // For now, we're just going to provide the traditional console.log
      return console.log;
    }
  }
}
