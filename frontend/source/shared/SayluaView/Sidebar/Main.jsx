import React, { Component } from 'react';
import { Link } from 'react-router-dom';

import { pluralize } from 'utils';
import PetAvatarView from 'shared/PetAvatarView';
import LoginForm from 'modules/Users/forms/LoginForm';

import './Sidebar.scss';


export default class Sidebar extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    let loggedIn = false;
    if (!loggedIn) {
      return (
        <div id="sidebar" className="sidebar">
          <div className="sidebar-section sidebar-login-form">
            <h3>Login to Saylua</h3>
            <LoginForm id="sidebar-login-form" compact />
          </div>
        </div>
      );
    }
    return (
      <div id="sidebar" className="sidebar">
        <PetAvatarView id="avatar-section" className="sidebar-section" user={ true } />
        <div id="user-info-section" className="sidebar-section">
          <p>You are User</p>
          <p>Your companion is <Link to="/companion">Companion Name</Link></p>
          <p>
            <img src="/static/img/icons/weather_clouds.png" />
            <Link to="/bank/"> { pluralize(5, 'Cloud Coin') } </Link>
          </p>
          <p>
            <img src="/static/img/icons/star_1.png" />
            <Link to="/bank/"> { pluralize(1, 'Star Shard') } </Link>
          </p>
        </div>
      </div>
    );
  }
}
