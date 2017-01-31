import {hasClass, removeClass, addClass, swapClass} from 'Utils';
import CheckAll from 'Plugins/CheckAll';
import FormValidation from 'Plugins/FormValidation/Main';
import './Notifications';


window.addEventListener('load', function () {
  window.addEventListener('scroll', fixNavbar);

  // Get all of the right navbar links and bind click events to them
  initializeDropMenus(document.getElementById('navigation-right'),
    document.getElementById('dropdown-right'));

  initializeDropMenus(document.getElementById('navigation-text-links'));

  // Bind dom behavior libraries to specific classes. Perhaps one day this
  // could be replace with webcomponents.
  let formValidation = new FormValidation('.validated-form');
  let checkAll = new CheckAll('.check-all');

  bindTabTyping('.tabs-allowed');
});

// Allow tabs to be allowed in text fields. This is useful for allowing users
// to edit code such as CSS.
function bindTabTyping(selector) {
  var inputs = document.querySelectorAll(selector);
  for (var i = 0; i < inputs.length; i++) {
    inputs[i].addEventListener('keydown', function (e) {
      if (e.keyCode == 9 || e.which == 9) {
          e.preventDefault();
          var s = this.selectionStart;
          this.value = this.value.substring(0, this.selectionStart)
            + "\t" + this.value.substring(this.selectionEnd);
          this.selectionEnd = s + 1;
      }
    });
  }
}

// Make navigation bar stay at the top
function fixNavbar(e) {
  var top = document.getElementById("banner").offsetHeight;
  if (document.body.scrollTop > top ||
    document.documentElement.scrollTop > top) {
    addClass(document.getElementById("navbar"), "navbar-fixed");
  } else {
    removeClass(document.getElementById("navbar"), "navbar-fixed");
  }
}

function initializeDropMenus(navigation, parentMenu) {
  if (!navigation) return;

  var menu = parentMenu;
  var links = navigation.getElementsByClassName('block-link');
  var sections = navigation.getElementsByClassName('menu');

  // For through right navigation links and attach listeners to them
  for (var i = 0; i < links.length; i++) {
    links[i].addEventListener('click', function changeMenu(e) {
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
    swapClass(menu, 'shown', 'hidden');
    document.body.removeEventListener('click', closeOnOutsideClick, false);
  }

  function showMenu(section) {
    // Make only the currently selected link highlighted
    for (var i = 0; i < links.length; i++) {
      if (links[i].getAttribute('data-section') == section) {
        addClass(links[i], 'active');
      } else {
        removeClass(links[i], 'active');
      }
    }

    // Iterate through all menus and close out ones other than the one showing
    for (var i = 0; i < sections.length; i++) {
      if (sections[i].id == section) {
        swapClass(sections[i], 'hidden', 'shown');
        if (!parentMenu) {
          menu = sections[i];
        }
      } else {
        swapClass(sections[i], 'shown', 'hidden');
      }
    }

    swapClass(menu, 'hidden', 'shown');
    document.body.addEventListener('click', closeOnOutsideClick);
  }

  function closeOnOutsideClick (e) {
    var target = e.target;
    if (!navigation.contains(target) && !menu.contains(target)) {
      hideMenu();
    }
  }
}
