import Inferno from 'inferno';
import Component from 'inferno-component';

import './Navbar.scss';

import Dropdown from './Dropdown';
import RightMenu from './RightMenu';
import Searchbar from './Searchbar';

export default class Navbar extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    let loggedIn = false;
    return (
      <div id="navbar-container" className="navbar-container">
        <div id="navbar" className="navbar">
          <div id="navbar-inner-container" className="navbar-inner-container">
            <div className="sidebar-filler"></div>
            <a href="/" className="navbar-block navbar-link" title="Home">
              <i className="fa fa-fw fa-home" aria-hidden="true"></i>
            </a>

            <Dropdown icon="fa-globe" name="Site" title="General Saylua Stuff" />

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

            <RightMenu />
          </div>
        </div>
      </div>
    );
  }
}
