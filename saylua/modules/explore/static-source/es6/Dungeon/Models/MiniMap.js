import BaseModel from "./BaseModel";

// VERY ugly band-aid. FIX THIS ASAP
// This should really be a redux reducer or similar. Instead of doing that,
// we're going to band-aid with this for now to delay adding extra libraries.
// (We WILL eventually have to do this as we grow in complexity)

export default class MiniMap extends BaseModel {
  constructor() {
    super();

    this.state = {
      "map": false
    };
  }

  get() {
    return this.state.map;
  }

  set(map) {
    this.state.map = map;
    this.triggerUpdate();
  }
}
