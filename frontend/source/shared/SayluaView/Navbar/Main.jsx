import React, { Component } from 'react';

import './Navbar.scss';

import Dropdown from './Dropdown';
import RightMenu from './RightMenu';
import Searchbar from './Searchbar';

import { dropdownContent } from './DropdownContent';

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

            {
              dropdownContent.map((menu, i) => {
                return <Dropdown key={ i.toString() } icon={ menu.icon }
                  name={ menu.name } content={ menu.content } />
              })
            }

            <Searchbar />

            <RightMenu />
          </div>
        </div>
      </div>
    );
  }
}
