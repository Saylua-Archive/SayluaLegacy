export function canonize(name) {
  name = name.replace(/(\s|\W)+/, '_');
  return name.toLowerCase();
}

export function pluralize(count, singular_noun, plural_noun) {
  if (!plural_noun) {
    plural_noun = singular_noun + 's';
  }
  if (count == 1) {
    return formatNumber(count) + ' ' + singular_noun
  }
  return formatNumber(count) + ' ' + plural_noun
}

// https://stackoverflow.com/questions/2901102/how-to-print-a-number-with-commas-as-thousands-separators-in-javascript
export function formatNumber(n) {
  return n.toLocaleString('en-IN');
}

// http://stackoverflow.com/questions/1026069/capitalize-the-first-letter-of-string-in-javascript
export function capitalizeFirst(string) {
  return string.charAt(0).toUpperCase() + string.slice(1);
}

// http://stackoverflow.com/questions/5767325/how-to-remove-a-particular-element-from-an-array-in-javascript
export function arrayRemove(arr, item) {
  for (var i = arr.length; i--;) {
    if (arr[i] === item) {
      arr.splice(i, 1);
      return true;
    }
  }
  return false;
}

// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/includes#Polyfill
if (!Array.prototype.includes) {
  Array.prototype.includes = function(searchElement /*, fromIndex*/ ) {
    'use strict';
    var O = Object(this);
    var len = parseInt(O.length, 10) || 0;
    if (len === 0) {
      return false;
    }
    var n = parseInt(arguments[1], 10) || 0;
    var k;
    if (n >= 0) {
      k = n;
    } else {
      k = len + n;
      if (k < 0) {k = 0;}
    }
    var currentElement;
    while (k < len) {
      currentElement = O[k];
      if (searchElement === currentElement ||
         (searchElement !== searchElement && currentElement !== currentElement)) { // NaN !== NaN
        return true;
      }
      k++;
    }
    return false;
  };
}

// https://stackoverflow.com/questions/8578617/inject-a-script-tag-with-remote-src-and-wait-for-it-to-execute#8578840
export function injectScript(src) {
  return new Promise((resolve, reject) => {
    const script = document.createElement('script');
    script.async = true;
    script.src = src;
    script.addEventListener('load', () => resolve());
    script.addEventListener('error', () => reject('Error loading script.'));
    script.addEventListener('abort', () => reject('Script loading aborted.'));
    document.head.appendChild(script);
  });
}

// http://stackoverflow.com/a/105074/784831
export function uuid() {
  function s4() {
    return Math.floor((1 + Math.random()) * 0x10000).toString(16).substring(1);
  }

  return s4() + s4() + '-' + s4() + '-' + s4() + '-' + s4() + '-' + s4() + s4() + s4();
}
