import {addClass} from 'Utils';

window.addEventListener('load', function () {
  var notificationCloseButtons = document.querySelectorAll('.notification a.close-button');

  for (var i = 0; i < notificationCloseButtons.length; i++) {
    var el = notificationCloseButtons[i];

    el.addEventListener("click", function(e) {
      e.preventDefault();

      var notification = e.target.parentElement;
      addClass(notification, "notification-fadeup");

      setTimeout(function() {
        notification.parentElement.removeChild(notification);
      }.bind(this), 1000);
    });
  }
});
