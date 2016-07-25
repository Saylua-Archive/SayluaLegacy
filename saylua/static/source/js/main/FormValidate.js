// Depends on utils.js
var _FormValidation = (function FormValidation() {
  var validatorList = {
    'required': {
      'error': '<field> is required. ',
      'validator':  function (input) {
        return input;
      }
    },
    'not_empty': {
      'error': '<field> cannot be only spaces. ',
      'validator':  function (input) {
        return /\S/.test(input);
      }
    },
    'min': {
      'error': '<field> cannot be shorter than <1> characters. ',
      'validator': function (input, length) {
        return input.length >= length;
      }
    },
    'max': {
      'error': '<field> cannot be longer than <1> characters. ',
      'validator': function (input, length) {
        return input.length <= length;
      }
    },
    'username_chars': {
      'error': '<field> may only contain letters, numbers, or these special characters: _.+!*()- ',
      'validator': function (input) {
        var reg = new RegExp('^[A-Za-z0-9_.+!*()-]+$');
        return reg.test(input);
      }
    },
    'no_repeated_underscores': {
      'error': '<field> may not contain two underscores in a row. ',
      'validator': function (input) {
        return input.indexOf('__') < 0;
      }
    },
    'match_password': {
      'error': 'Passwords must match. ',
      'validator': function (input, match_id) {
        return document.getElementById(match_id).value === input;
      }
    },
    'email': {
      'error': '<field> must be a valid email. ',
      'validator': function (input) {
        return /\S+@\S+\.\S+/.test(input);
      }
    }
  };

  return function FormValidationConstructor() {
    this.bind = function(selector) {
      var forms = document.querySelectorAll(selector);
      for (var i = 0; i < forms.length; i++) {
        forms[i].addEventListener('submit', _formSubmitListener); // End event listener
      }
    };
  };

  function _formSubmitListener(e) {
    var errCount = 0;
    var form = e.currentTarget;
    var fields = form.querySelectorAll('input, textarea');
    var errorContainer = document.getElementById(form.getAttribute('data-error-id'));
    if (errorContainer) {
      errorContainer.innerHTML = '';
    }
    for (var j = 0; j < fields.length; j++) {
      var validators = fields[j].getAttribute('data-validators');
      var errors = fields[j].getAttribute('data-errors');
      if (errors) {
        errors = JSON.parse(errors);
      }
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
            if (errors && validatorName in errors) {
              err = errors[validatorName];
            } else {
              err = validatorList[validatorName].error.replace('<field>', field.replace(/[_-]/g, ' '));
            }
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
}());

var FormValidation = new _FormValidation();
