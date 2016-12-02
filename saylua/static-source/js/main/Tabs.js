// Depends on utils.js
var _Tabs = (function Tabs() {
  return function TabsConstructor() {
    this.bind = function(selector) {
      var tabContainers = document.querySelectorAll(selector);
      for (var i = 0; i < tabContainers.length; i++) {
        processTabs(tabContainers[i]);
      }
    };
  };

  function processTabs(container) {
    var tabs = container.getElementsByClassName('tab');
    for (var i = 0; i < tabs.length; i++) {
      if (!hasClass(tabs[i], 'selected')) {
        // Hide all tabs except the selected one
        var target = document.getElementById(tabs[i].href.split("#")[1]);
        addClass(target, 'hidden');
      }

      tabs[i].addEventListener('click', function (e) {
        e.preventDefault();
        var currentTab = e.currentTarget;
        for (var j = 0; j < tabs.length; j++) {
          var target = document.getElementById(tabs[j].href.split("#")[1]);
          if (tabs[j] != currentTab) {
            addClass(target, 'hidden');
            removeClass(tabs[j], 'selected');
          } else {
            removeClass(target, 'hidden');
            addClass(tabs[j], 'selected');
          }
        }
      });
    }
  }
}());

var Tabs = new _Tabs();
