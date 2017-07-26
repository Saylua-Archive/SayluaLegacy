import Inferno from 'inferno';
import Component from 'inferno-component';

export default class RightMenu extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    let loggedIn = false;
    let notificationsCount = 1;
    let messagesCount = 0;

    if (!loggedIn) {
      return (
        <div className="navbar-block">
          <a href="/login/" className="navbar-link">
            <i className="fa fa-fw fa-user" aria-hidden="true" title="User"></i>
          </a>
        </div>
      );
    }
    return (
      <div id="navbar-user-links" className="navbar-user-links navbar-block">
        <a href="/user/tiff/" className="navbar-link" data-section="user-menu">
          <i className="fa fa-fw fa-user" aria-hidden="true" title="User"></i>
        </a>
        <a href="/notifications/" className="navbar-link" data-section="notifications-menu">
          <i className="fa fa-fw fa-bell" aria-hidden="true" title="Notifications"></i>
          { notificationsCount > 0 &&
            <span className="alert-number">
              { notificationsCount > 99 ? '99+' : notificationsCount }
            </span>
          }
        </a>
        <a href="/messages/" className="navbar-link" data-section="messages-menu">
          <i className="fa fa-fw fa-envelope" aria-hidden="true" title="Messages"></i>
            { messagesCount > 0 &&
              <span className="alert-number">
                { messagesCount > 99 ? '99+' : messagesCount }
              </span>
            }
        </a>
        <div id="dropdown-user-menu" className="dropdown-menu">
          <div id="user-menu" className="menu">
            <h3>Logged in as #USERNAME</h3>
            <a href="#USER_URL">
              <img src="/static/img/icons/user.png" alt="user" title="My Profile" aria-label="My Profile" />
              My Profile
            </a>
            <a href="/settings/">
              <img src="/static/img/icons/cog.png" alt="cog" title="Settings" aria-label="Settings" />
              Account Settings
            </a>
            <span className="dropdown-separator"></span>
            <a href="/achievements/#USERNAME/">
              <img src="/static/img/icons/award_star_gold.png" alt="ribbon" title="Achievements" aria-label="Achievements" />
              My Achievements
            </a>
            <span className="dropdown-separator"></span>
            <a href="/logout/">
              <img src="/static/img/icons/lock_unlock.png" alt="unlock" title="Logout" aria-label="Logout" />
              Logout
            </a>
          </div>
          <div id="notifications-menu" className="menu">
            <h3>Latest Notifications</h3>
            <span className="dropdown-separator"></span>
            <a href="/notifications/">
              <img src="/static/img/icons/star_1.png" alt="star" title="All Notifications" aria-label="All Notifications" />
              View All Notifications
            </a>
          </div>
          <div id="messages-menu" className="menu">
            <h3>Latest Messages</h3>
            <span className="dropdown-separator"></span>
            <a href="/messages/">
              <img src="/static/img/icons/email.png" alt="mail" title="All Messages" aria-label="All Messages" />
              View All Messages
            </a>
          </div>
        </div>
      </div>
    );
  }
}
