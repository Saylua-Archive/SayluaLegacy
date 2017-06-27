import {hasClass, removeClass, addClass, swapClass} from 'Utils';

// Make navigation bar stay at the top.
export function fixNavbar(e) {
  let top = document.getElementById("banner").offsetHeight;
  if (document.body.scrollTop > top ||
    document.documentElement.scrollTop > top) {
    addClass(document.getElementById("navbar"), "navbar-fixed");
  } else {
    removeClass(document.getElementById("navbar"), "navbar-fixed");
  }
}

export function initializeDropMenus(navigation, parentMenu) {
  if (!navigation) return;

  let menu = parentMenu;
  let links = navigation.getElementsByClassName('navbar-link');
  let sections = navigation.getElementsByClassName('menu');

  // For through right navigation links and attach listeners to them
  for (let i = 0; i < links.length; i++) {
    links[i].addEventListener('click', function changeMenu(e) {
      e.preventDefault();
      let link = e.currentTarget;

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
    for (let i = 0; i < links.length; i++) {
      removeClass(links[i], 'active');
    }
    swapClass(menu, 'shown', 'hidden');
    document.body.removeEventListener('click', closeOnOutsideClick, false);
  }

  function showMenu(section) {
    // Make only the currently selected link highlighted
    for (let i = 0; i < links.length; i++) {
      if (links[i].getAttribute('data-section') == section) {
        addClass(links[i], 'active');
      } else {
        removeClass(links[i], 'active');
      }
    }

    // Iterate through all menus and close out ones other than the one showing
    for (let i = 0; i < sections.length; i++) {
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
    let target = e.target;
    if (!navigation.contains(target) && !menu.contains(target)) {
      hideMenu();
    }
  }
}
