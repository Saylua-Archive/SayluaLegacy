var _CheckAll = (function CheckAll() {
  return function CheckAllConstructor() {
    this.bind = function(selector) {
      var triggers = document.querySelectorAll(selector);
      for (var i = 0; i < triggers.length; i++) {
        if (isCheckbox(triggers[i])) {
          // Currently only checkboxes are supported
          triggers[i].addEventListener('click', function (e) {
            var targetName = e.target.getAttribute('data-name');
            var boxes = document.getElementsByName(targetName);
            for (var j = 0; j < boxes.length; j++) {
              boxes[j].checked = e.target.checked;
            }
          });
        }
      }
    };
  };

  function isCheckbox(el) {
    return el.type && el.type === 'checkbox';
  }
}());

var CheckAll = new _CheckAll();
