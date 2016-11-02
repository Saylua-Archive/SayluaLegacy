// VERY ugly band-aid. FIX THIS ASAP
// This should really be a redux reducer or similar. Instead of doing that,
// we're going to band-aid with this for now to delay adding extra libraries.
// (We WILL eventually have to do this as we grow in complexity)
export default class MiniMap {
  constructor() {
    this.state = {
      "map": false
    };
  }

  bindComponent(component) {
    this.state.component = component;
  }

  get() {
    return this.state.map;
  }

  set(map) {
    this.state.map = map;
    if (this.state.component !== undefined) {
      let triggerUpdate = (this.state.component.triggerUpdate == undefined) ? true : !this.state.component.triggerUpdate;
      this.state.component.setState({
        "triggerUpdate": triggerUpdate
      });
    }
  }
}
