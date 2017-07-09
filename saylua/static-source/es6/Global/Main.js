import CheckAll from 'Plugins/CheckAll';
import FormValidation from 'Plugins/FormValidation/Main';

import {initializeNotifications} from './Notifications';
import {fixNavbar, initializeDropMenus} from './Navbar';


// Make navbar stay at top.
fixNavbar();
window.addEventListener('scroll', fixNavbar);

// Get all of the right navbar links and bind click events to them.
initializeDropMenus(document.getElementById('navbar-user-links'),
  document.getElementById('dropdown-user-menu'));

let links = document.getElementsByClassName('navbar-main-links');
for (let i = 0; i < links.length; i++) {
  initializeDropMenus(links[i]);
}

// Bind dom behavior libraries to specific classes. Perhaps one day this
// could be replaced with web components.
new FormValidation('.validated-form');
new CheckAll('.check-all');

// Make notificaitons able to be dismissed.
initializeNotifications();
