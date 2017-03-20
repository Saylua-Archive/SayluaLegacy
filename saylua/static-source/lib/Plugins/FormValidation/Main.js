import {capitalizeFirst, removeClass, addClass} from 'Utils';
import {validatorList} from './Validators';

export default class FormValidation {
  constructor(selector) {
    if (selector) {
      this.bind(selector);
    }
  }

  // Takes in a DOM selector for elements that should have form validation
  // applied, parses the forms for information on the validators, and applies
  // listeners to changing inputs/submit.
  bind(selector) {
    let forms = document.querySelectorAll(selector);
    for (let i = 0; i < forms.length; i++) {
      let f = new _ValidatedForm(forms[i]);
      f.attachListeners();
    }
  }
}

class _ValidatedForm {
  // Parse a form and store all its
  constructor(form) {
    this.form = form;
    this.errorElementMap = {};

    let errorElements = form.getElementsByClassName('form-error');
    for (let i = 0; i < errorElements.length; i++) {
      let e = errorElements[i];
      this.errorElementMap[e.getAttribute('data-field-name')] = e;
    }
  }

  attachListeners() {
    let fields = this.form.querySelectorAll('input, textarea');
    for (let i = 0; i < fields.length; i++) {
      // Add event listeners for validating users' input when they unfocus.
      let listenTo = 'blur';
      if (fields[i].type == 'checkbox') {
        listenTo = 'change';
      }
      fields[i].addEventListener(listenTo, this._validateField.bind(this, fields[i]));
    }

    let self = this;
    this.form.addEventListener('submit', function (e) {
      if (!self._validateAllFields()) {
        e.preventDefault();
        return false;
      }
      return true;
    });
  }

  // Returns false if validation failed.
  _validateField(field) {
    let validators = field.getAttribute('data-slform-validators');
    if (!validators) {
      // Can't fail validation that doesn't exist...
      return true;
    }
    validators = validators.split(" ");
    let err = false;
    for (let i = 0; !err && i < validators.length; i++) {
      let params = validators[i].split(":");
      let validatorName = params[0];
      if(!validatorList[validatorName]) {
        throw "Invalid validator type: " + validatorName;
      }

      let value = field.value;
      if (field.type == 'checkbox') {
        value = field.checked;
      }

      // [input, p1, p2, ...]
      params = [value].concat(params.slice(1));

      // Check to see if the validation fails.
      if (!validatorList[validatorName].validator.apply(this, params)) {
        err = validatorList[validatorName].error;

        // Check to see if the HTML overwrites the default validator error message.
        let message = field.getAttribute('data-slform-' + validatorName + '-message');
        if (message) {
          err = message;
        }

        // Error messages can be formatted to reference the field name or the
        // validation function parameters.
        let niceFieldName = capitalizeFirst(field.name).replace(/[_-]/g, ' ');
        err = err.replace('<field>', niceFieldName);
        for (let l = 1; l < params.length; l++) {
          err = err.replace('<' + l + '>', params[l]);
        }
      }
    }

    // Render the error message.
    if (this.errorElementMap[field.name]) {
      this.errorElementMap[field.name].innerHTML = err || '';
    }
    return !err;
  }

  _validateAllFields(e) {
    let hasError = false;
    let fields = this.form.querySelectorAll('input, textarea');

    for (let j = 0; j < fields.length; j++) {
      hasError = !this._validateField(fields[j]) || hasError;
    }

    return !hasError;
  }
}
