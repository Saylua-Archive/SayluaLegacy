export default class CheckAll {
  constructor(selector) {
    if (selector) {
      this.bind(selector);
    }
  }

  bind(selector) {
    var triggers = document.querySelectorAll(selector);
    for (var i = 0; i < triggers.length; i++) {
      if (this.isCheckbox(triggers[i])) {
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
  }

  isCheckbox(el) {
    return el.type && el.type === 'checkbox';
  }
}
