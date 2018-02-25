import React, { Component } from 'react';

import { Link } from 'react-router-dom';

import './UserLink.scss';

export default class UserLink extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    let user = this.props.user;
    if (!user) {
      return;
    }
    let url = '/';
    let titleClass = 'title-moderator';
    let name = 'username';
    let status = 'pies';
    return (
      <span>
        <Link to={ url } className={ titleClass }>{ name }</Link>
          { status && <small>{ status }</small> }
      </span>
    );
  }
}
