import {capitalizeFirst, removeClass, addClass} from 'Utils';
import {validatorList} from './Validators';

export default class FormValidation {
  constructor(selector) {
    if (selector) {
      this.bind(selector);
    }
  }

  bind(selector) {
    let forms = document.querySelectorAll(selector);
    for (let i = 0; i < forms.length; i++) {
      forms[i].addEventListener('submit', this._formSubmitListener); // End event listener
    }
  }

  _formSubmitListener(e) {
    let errCount = 0;
    let form = e.currentTarget;
    let fields = form.querySelectorAll('input, textarea');

    // DOM element for showing all errors in one place.
    let errorContainer = document.getElementById(form.getAttribute('data-error-id'));
    let errorFields = form.getElementsByClassName('form-error');
    let errorFieldMap = {};
    for (let i = 0; i < errorFields.length; i++) {
      let field = errorFields[i];
      if (field.getAttribute('data-field-name')) {
        // Oh noes, side effects in my reduce! D:
        field.innerHTML = '';
        errorFieldMap[field.getAttribute('data-field-name')] = field;
      }
    }

    if (errorContainer) {
      errorContainer.innerHTML = '';
    }
    for (let j = 0; j < fields.length; j++) {
      let validators = fields[j].getAttribute('data-slform-validators');
      if (validators) {
        removeClass(fields[j], 'error');
        validators = validators.split(" ");
        let noErrors = true;
        for (let k = 0; noErrors && k < validators.length; k++) {
          let params = validators[k].split(":");
          let validatorName = params[0];
          if(!validatorList[validatorName]) {
            throw "Invalid validator type: " + validatorName;
          }

          let value = fields[j].value;
          if (fields[j].type == 'checkbox') {
            value = fields[j].checked;
          }

          // [input, p1, p2, ...]
          params = [value].concat(params.slice(1));

          // Check to see if the validation fails
          if (!validatorList[validatorName].validator.apply(this, params)) {
            addClass(fields[j], 'error');
            let field = capitalizeFirst(fields[j].name);
            let err;
            let message = fields[j].getAttribute('data-slform-' + validatorName + '-message');
            if (message) {
              err = message;
            } else {
              err = validatorList[validatorName].error;
            }
            err = err.replace('<field>', field.replace(/[_-]/g, ' '));
            for (let l = 1; l < params.length; l++) {
              err = err.replace('<' + l + '>', params[l]);
            }
            errCount++;
            noErrors = false;

            if (errorContainer) {
              errorContainer.innerHTML += '<p class="error">' + err + '</p>';
            }

            if (errorFieldMap[fields[j].name]) {
              errorFieldMap[fields[j].name].innerHTML = err;
            }
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
