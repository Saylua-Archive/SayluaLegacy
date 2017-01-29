import {capitalizeFirst, removeClass, addClass} from 'Utils';
import {validatorList} from './Validators';

export default class FormValidation {
  constructor(selector) {
    if (selector) {
      this.bind(selector);
    }
  }

  bind(selector) {
    var forms = document.querySelectorAll(selector);
    for (var i = 0; i < forms.length; i++) {
      forms[i].addEventListener('submit', this._formSubmitListener); // End event listener
    }
  }

  _formSubmitListener(e) {
    var errCount = 0;
    var form = e.currentTarget;
    var fields = form.querySelectorAll('input, textarea');
    var errorContainer = document.getElementById(form.getAttribute('data-error-id'));
    if (errorContainer) {
      errorContainer.innerHTML = '';
    }
    for (var j = 0; j < fields.length; j++) {
      var validators = fields[j].getAttribute('data-slform-validators');
      if (validators) {
        removeClass(fields[j], 'error');
        validators = validators.split(" ");
        var noErrors = true;
        for (var k = 0; noErrors && k < validators.length; k++) {
          var params = validators[k].split(":");
          var validatorName = params[0];
          if(!validatorList[validatorName]) {
            throw "Invalid validator type: " + validatorName;
          }

          var value = fields[j].value;
          if (fields[j].type == 'checkbox') {
            value = fields[j].checked;
          }

          // [input, p1, p2, ...]
          params = [value].concat(params.slice(1));

          // Check to see if the validation fails
          if (!validatorList[validatorName].validator.apply(this, params)) {
            addClass(fields[j], 'error');
            var field = capitalizeFirst(fields[j].name);
            var err;
            var message = fields[j].getAttribute('data-slform-' + validatorName + '-message');
            if (message) {
              err = message;
            } else {
              err = validatorList[validatorName].error;
            }
            err = err.replace('<field>', field.replace(/[_-]/g, ' '));
            for (var l = 1; l < params.length; l++) {
              err = err.replace('<' + l + '>', params[l]);
            }
            errCount++;
            noErrors = false;
            errorContainer.innerHTML += '<p class="error">' + err + '</p>';
          }
        }
      }
    }
    if (errCount > 0) {
      e.preventDefault();
      return false;
    }
    return true;
  }
}
