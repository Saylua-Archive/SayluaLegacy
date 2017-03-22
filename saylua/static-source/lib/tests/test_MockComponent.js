import * as assert from "assert";

import MockComponent from "./MockComponent";


describe('MockComponent', function() {
  it('should initialize without error', (done) => {
    let component = new MockComponent();
    assert.ok(component);
    done();
  });


  it('should initialize correctly with props', (done) => {
    let component = new MockComponent({ "property": "value" });

    assert.deepEqual(component.props, { "property": "value" });
    done();
  });


  it('should initialize correctly with props and defaultState', (done) => {
    let component = new MockComponent({ "property": "value" }, { "initial": true });

    assert.deepEqual(component.props, { "property": "value" });
    assert.deepEqual(component.state, { "initial": true });

    done();
  });


  it('should update state properly', (done) => {
    let component = new MockComponent({}, { "initial": true });
    let expectedValues = {
      "initial": true,
      "a": true,
      "b": 10,
      "c": "string"
    };

    component.setState({ "a": true });
    component.setState({
      "b": 10,
      "c": "string"
    });

    assert.deepEqual(component.state, expectedValues);

    for (let key of Object.keys(expectedValues)) {
      assert.strictEqual(component.state[key], expectedValues[key]);
    }

    done();
  });

});
