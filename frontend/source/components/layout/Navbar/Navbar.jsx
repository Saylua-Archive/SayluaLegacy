import Inferno from 'inferno';
import Component from 'inferno-component';

import './Navbar.scss';

import Searchbar from './Searchbar';

export default class Navbar extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    let loggedIn = false;
    let rightMenu = (
      <div className="navbar-block">
        <a href="/login/" className="navbar-link">
          <i className="fa fa-fw fa-user" aria-hidden="true" title="User"></i>
        </a>
      </div>
    );
    if (loggedIn) {
      let notificationsCount = 1;
      let messagesCount = 0;
      rightMenu = (
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
    return (
      <div id="navbar-container" className="navbar-container">
        <div id="navbar" className="navbar">
          <div id="navbar-inner-container" className="navbar-inner-container">
            <div className="sidebar-filler"></div>
            <a href="/" className="navbar-block navbar-link" title="Home">
              <i className="fa fa-fw fa-home" aria-hidden="true"></i>
            </a>

            <div className="navbar-block navbar-main-links">
              <a href="/" className="navbar-link" data-section="site-menu">
                <i className="fa fa-fw fa-globe" aria-hidden="true" title="Site"></i>
                <label>Site</label>
              </a>
              <div className="left-menu dropdown-menu menu" id="site-menu">
                <h3>General Saylua Stuff</h3>
                <a href="/"><img src="/static/img/icons/house.png" /> My House</a>
                <a href="/news/"><img src="/static/img/icons/newspaper.png" /> Saylua News</a>
                <a href="/inventory/"><img src="/static/img/icons/box.png" /> My Inventory</a>
              </div>
            </div>
            <div className="navbar-block navbar-main-links">
              <a href="/games/" className="navbar-link" data-section="play-menu">
                <i className="fa fa-fw fa-paw" aria-hidden="true" title="Play"></i>
                <label>Play</label>
              </a>
              <div className="left-menu dropdown-menu menu" id="play-menu">
                <h3>Games and Fun</h3>
                <a href="/adventure/">
                  <img src="/static/img/icons/compass.png" alt="compass" title="Adventure" aria-label="Adventure" />
                  Adventure
                </a>
                <a href="/town/">
                  <img src="/static/img/icons/group.png" alt="people" title="Town Square" aria-label="Town Square" />
                  Town Square
                </a>
                <a href="/arcade/">
                  <img src="/static/img/icons/joystick.png" alt="joystick" title="Games" aria-label="Games" />
                  The Arcade
                </a>
              </div>
            </div>
            <div className="navbar-block navbar-main-links">
              <a href="/shops/" className="navbar-link" data-section="trade-menu">
                <i className="fa fa-fw fa-suitcase" aria-hidden="true" title="Trade"></i>
                <label>Trade</label>
              </a>
              <div className="left-menu dropdown-menu menu" id="trade-menu">
                <h3>Buy and Sell</h3>
                <a href="/shop/general/">
                  <img src="/static/img/icons/tag_blue.png" alt="tag" title="Sales" aria-label="Sales" />
                  General Store
                </a>
                <a href="/bank/">
                  <img src="/static/img/icons/coins.png" alt="coins" title="Bank" aria-label="Bank" />
                  Bank of Saylua
                </a>
                <a href="/market/">
                  <img src="/static/img/icons/direction.png" alt="crossroads" title="Market" aria-label="Market" />
                   Player Market
                 </a>
                <span className="dropdown-separator"></span>
                <a href="/starshards/">
                  <img src="/static/img/icons/star_1.png" alt="star" title="Star Shards" aria-label="Star Shards" />
                  Purchase Star Shards
                </a>
              </div>
            </div>
            <div className="navbar-block navbar-main-links">
              <a href="/forums/" className="navbar-link" data-section="community-menu">
                <i className="fa fa-fw fa-comments" aria-hidden="true" title="Community"></i>
                <label>Community</label>
              </a>
              <div className="left-menu dropdown-menu menu" id="community-menu">
                <h3>Interact with Others</h3>
                <a href="/forums/">
                  <img src="/static/img/icons/comment.png" alt="speech bubble" title="Forums" aria-label="Forums" />
                  Forums
                </a>
                <a href="https://discord.gg/CPet6aq" target="_blank" rel="noopener">
                  <img src="/static/img/icons/transmit.png" alt="transmission" title="Chat" aria-label="Chat" />
                  Discord Server
                </a>
                <span className="dropdown-separator"></span>
                <a href="/reserve/">
                  <img src="/static/img/icons/heart.png" alt="heart" title="Reserve" aria-label="Reserve" />
                  Pet Reserve
                </a>
              </div>
            </div>
            <div className="navbar-block navbar-main-links">
              <a href="/help/" className="navbar-link" data-section="archives-menu">
                <i className="fa fa-fw fa-book" aria-hidden="true" title="Archives"></i>
                <label>Archives</label>
              </a>
              <div className="left-menu dropdown-menu menu" id="archives-menu">
                <h3>Learn About Saylua</h3>
                <a href="/species/">
                  <img src="/static/img/icons/clipboard_text.png" alt="clipboard" title="Species Guide" aria-label="Species Guide" />
                  Species Guide
                </a>
                <a href="/items/">
                  <img src="/static/img/icons/drawer.png" alt="drawer" title="Item Database" aria-label="Item Database" />
                  Item Database
                </a>
                <a href="/knowledge/">
                  <img src="/static/img/icons/find.png" alt="magnifying glass" title="Knowledge Base" aria-label="Knowledge Base" />
                  Knowledge Base
                </a>
                <span className="dropdown-separator"></span>
                <a href="/museum/">
                  <img src="/static/img/icons/palette.png" alt="palette" title="Museum" aria-label="Museum" />
                  The Museum
                </a>
              </div>
            </div>

            <Searchbar />

            { rightMenu }
          </div>
        </div>
      </div>
    );
  }
}
