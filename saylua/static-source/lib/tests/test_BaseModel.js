import * as assert from "assert";
import Component from "inferno-component";

import BaseModel from "../Models/BaseModel.js";

describe('Models', function() {
  describe('BaseModel', function() {
    it('should initialize without error', (done) => {
      let model = new BaseModel();
      assert.ok(model);
      done();
    });
  });
});
