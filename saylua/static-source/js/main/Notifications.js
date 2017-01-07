window.addEventListener('load', function () {
  var notifications = document.querySelectorAll('.notification a.close-button');

  for (var i = 0; i < notifications.length; i++) {
    var el = notifications[i];

    el.addEventListener("click", function(e) {
      e.preventDefault();

      var notification = e.target.parentElement;
      addClass(notification, "notification-fadeup");

      setTimeout(function(){
        notification.parentElement.removeChild(notification);
      }, 1000);
    });
  }
});
