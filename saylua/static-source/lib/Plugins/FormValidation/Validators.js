export const validatorList = {
  'required': {
    'error': '<field> is required.',
    'validator': function (input) {
      return input;
    }
  },
  'notblank': {
    'error': '<field> cannot be only spaces.',
    'validator': function (input) {
      return /\S/.test(input);
    }
  },
  'min': {
    'error': '<field> cannot be shorter than <1> characters.',
    'validator': function (input, length) {
      return input.length >= length;
    }
  },
  'max': {
    'error': '<field> cannot be longer than <1> characters.',
    'validator': function (input, length) {
      return input.length <= length;
    }
  },
  'number': {
    'error': '<field> must be a number!',
    'validator': function (input) {
      return !isNaN(input);
    }
  },
  'atleast': {
    'error': '<field> must be at least <1>!',
    'validator': function (input, minval) {
      return input * 1 >= minval * 1;
    }
  },
  'regex': {
    'error': '<field> is incorrectly formatted.',
    'validator': function (input, regex) {
      var reg = new RegExp(regex);
      return reg.test(input);
    }
  },
  'equalto': {
    'error': '<field> must match <1>.',
    'validator': function (input, match_name) {
      return document.getElementsByName(match_name)[0].value === input;
    }
  },
  'isnot': {
    'error': '<field> cannot be <1>.',
    'validator': function (input, value) {
      return input != value;
    }
  },
};
