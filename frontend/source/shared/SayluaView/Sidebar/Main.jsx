import React, { Component } from 'react';

import { pluralize } from 'lib/Utils';

import './Sidebar.scss';

import PetAvatarView from 'shared/PetAvatarView';

// The main Saylua layout component.
export default class Sidebar extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    let loggedIn = true;
    return (
      <div id="sidebar" className="sidebar">
        <PetAvatarView id="avatar-section" className="sidebar-section" user={ true } />
        { loggedIn ? (
          <div id="user-info-section" className="sidebar-section">
            <p>You are User</p>
            <p>Your companion is <a href="/companion">Companion Name</a></p>
            <p>
              <img src="/static/img/icons/weather_clouds.png" />
              <a href="/bank/"> { pluralize(5, 'Cloud Coin') } </a>
            </p>
            <p>
              <img src="/static/img/icons/star_1.png" />
              <a href="/bank/"> { pluralize(1, 'Star Shard') } </a>
            </p>
          </div>
        ) : (
        <form id="sidebar-login-form" className="sidebar-section sidebar-login-form validated-form" action="/login/"
          method="post">
          <h3>Login to Saylua</h3>
          <table className="form-table center">
            <tr>
              <td>
                <small className="form-tip"></small>
              </td>
            </tr>
            <tr>
              <td>
                <small className="form-tip"></small>
              </td>
            </tr>
            <tr>
              <td>
                <input type="submit" className="small" value="Login!" name="login" />
              </td>
            </tr>
            <tr>
              <td>
                <p><a href="/login/recover/">Lost credentials?</a></p>
                <p><a href="/register/">Register!</a></p>
              </td>
            </tr>
          </table>
        </form>
        )}
      </div>
    );
  }
}
