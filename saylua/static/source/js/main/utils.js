// From http://jaketrent.com/post/addremove-classes-raw-javascript/
function hasClass(el, className) {
  if (el.classList)
    return el.classList.contains(className)
  else
    return !!el.className.match(new RegExp('(\\s|^)' + className + '(\\s|$)'))
}

function addClass(el, className) {
  if (el.classList)
    el.classList.add(className)
  else if (!hasClass(el, className)) el.className += " " + className
}

function removeClass(el, className) {
  if (el.classList)
    el.classList.remove(className)
  else if (hasClass(el, className)) {
    var reg = new RegExp('(\\s|^)' + className + '(\\s|$)')
    el.className = el.className.replace(reg, ' ')
  }
}

function swapClass(el, classA, classB) {
  removeClass(el, classA);
  addClass(el, classB);
}

// http://stackoverflow.com/questions/1026069/capitalize-the-first-letter-of-string-in-javascript
function capitalizeFirst(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

// http://stackoverflow.com/questions/8830839/javascript-dom-remove-element
function removeElement(el) {
  if (el) {
    el.parentNode.removeChild(el);
  }
}
