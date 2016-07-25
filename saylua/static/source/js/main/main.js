window.addEventListener('load', function () {
  window.addEventListener('scroll', fixNavbar);

  // Get all of the right navbar links and bind click events to them
  initializeRightMenu();

  // Form Validation
  FormValidation.bind('.validated-form');
});

// Make navigation bar stay at the top
function fixNavbar(e) {
  var top = document.getElementById("banner").offsetHeight;
  if (document.body.scrollTop > top ||
    document.documentElement.scrollTop > top) {
    addClass(document.getElementById("navbar"), "fixed");
  } else {
    removeClass(document.getElementById("navbar"), "fixed");
  }
}

function initializeRightMenu() {
  var navigation = document.getElementById('navigation-right');
  var menu = document.getElementById('dropdown-right');
  var links = navigation.getElementsByClassName('block-link');
  var sections = menu.getElementsByClassName('menu');

  // For through right navigation links and attach listeners to them
  for (var i = 0; i < links.length; i++) {
    links[i].addEventListener('click', function changeRightMenu(e) {
      e.preventDefault();
      var link = e.currentTarget;

      if (hasClass(link, 'active')) {
        // Clicking on a selected icon removes the menu
        hideMenu();
        removeClass(link, 'active');
      } else {
        showMenu(link.getAttribute('data-section'));
      }
    });
  }

  function hideMenu() {
    for (var i = 0; i < links.length; i++) {
      removeClass(links[i], 'active');
    }
    menu.style.display = 'none';
    document.body.removeEventListener('click', closeOnOutsideClick, false);
  }

  function showMenu(section) {
    for (var i = 0; i < links.length; i++) {
      if (links[i].getAttribute('data-section') == section) {
        addClass(links[i], 'active');
      } else {
        removeClass(links[i], 'active');
      }
    }
    for (var i = 0; i < sections.length; i++) {
      if (sections[i].id == section) {
        sections[i].style.display = 'block';
      } else {
        sections[i].style.display = 'none';
      }
    }
    menu.style.display = 'block';
    document.body.addEventListener('click', closeOnOutsideClick);
  }

  function closeOnOutsideClick (e) {
    var target = e.target;
    if (!navigation.contains(target) && !menu.contains(target)) {
      hideMenu();
    }
  }
}
