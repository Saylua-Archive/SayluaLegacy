import Inferno from 'inferno';

export const dropdownContent = [
  {
    'name': 'Site',
    'icon': 'fa-globe',
    'content': (
      <div className="dropdown-menu menu">
        <h3>General Saylua Stuff</h3>
        <a href="/">
          <img src="/static/img/icons/house.png" alt="house" title="My House" aria-label="My House" />
          My House
        </a>
        <a href="/news/">
          <img src="/static/img/icons/newspaper.png" alt="newspaper" title="The News" aria-label="The News" />
          Saylua News
        </a>
        <a href="/inventory/">
          <img src="/static/img/icons/box.png" alt="box" title="Inventory" aria-label="Inventory" />
          My Inventory
        </a>
      </div>
    )
  },
  {
    'name': 'Play',
    'icon': 'fa-paw',
    'content': (
      <div className="dropdown-menu menu">
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
    )
  },
  {
    'name': 'Trade',
    'icon': 'fa-suitcase',
    'content': (
      <div className="dropdown-menu menu">
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
    )
  },
  {
    'name': 'Community',
    'icon': 'fa-comments',
    'content': (
      <div className="dropdown-menu menu">
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
    )
  },
  {
    'name': 'Archives',
    'icon': 'fa-book',
    'content': (
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
    )
  },
];
