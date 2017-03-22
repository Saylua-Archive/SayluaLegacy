// MockComponent -> Testing lib.
// --------------------------------------
// Provides an extremely basic anologue to Inferno's Component
// functionality. Only meant to provide a minimal, library
// agnostic testing tool, not meant to be a complete replica.

export default class MockComponent {

  // Our constructor will be atypical in comparison to a normal Component
  // in that it will also take a default state parameter.
  constructor(defaultProps={}, defaultState={}) {
    this.props = defaultProps;
    this.state = defaultState;
  }


  setState(input) {
    for (let key of Object.keys(input)) {
      this.state[key] = input[key];
    }
  }
}
