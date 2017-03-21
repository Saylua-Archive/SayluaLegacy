import * as assert from "assert";

import BaseModel from "../Models/BaseModel.js";
import MockComponent from "./MockComponent";


describe('Models', function() {
  describe('BaseModel', function() {
    it('should initialize without error', (done) => {
      let model = new BaseModel();
      assert.ok(model);
      done();
    });


    it('should bind properly with a component', (done) => {
      // Nest model within a component, then bind that
      // model to said component.

      let model = new BaseModel();
      let component = new MockComponent({ model });

      model.bindComponent(component);
      assert.deepEqual(model.__components, [component]);

      // Attempt to bind a second component.

      let otherComponent = new MockComponent({ model });

      model.bindComponent(otherComponent);
      assert.deepEqual(model.__components, [component, otherComponent]);

      done();
    });


    it('should trigger updates in bound components', (done) => {
      let model = new BaseModel();
      let component = new MockComponent({ model });
      let otherComponent = new MockComponent({ model });

      model.bindComponent(component);
      model.bindComponent(otherComponent);

      // Trigger an update, see if the bound components have changed.

      model.triggerUpdate();
      assert.strictEqual(otherComponent.state.triggerUpdate, true);

      // Manually flip one of the states

      component.setState({ "triggerUpdate": false });
      model.triggerUpdate();

      assert.strictEqual(component.state.triggerUpdate, true);
      assert.strictEqual(otherComponent.state.triggerUpdate, false);

      done();
    });

    it('should trigger updates in pre-initialized bound components', (done) => {
      let model = new BaseModel();
      let component = new MockComponent({ model }, { "triggerUpdate": true });

      model.bindComponent(component);
      model.triggerUpdate();

      assert.strictEqual(component.state.triggerUpdate, false);

      done();
    });
  });
});
