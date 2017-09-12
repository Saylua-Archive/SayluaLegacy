import React, { Component } from 'react';

import { Link } from 'react-router-dom';

import './PetAvatarView.scss';


export default class PetAvatarView extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    let user = this.props.user;
    if (!user) {
      return;
    }
    return (
      <div className="pet-avatar-view">
        <div className="avatar-view">
          <Link to="">
            <img src="/static/img/avatar/base.png" alt="human avatar" title="'s Avatar'" aria-label="'s Avatar'" />
          </Link>
        </div>
        <Link to="" className="active-pet-view">
          <img src="/static/img/pets/loxi/common.png" className="active-pet-image" alt="active companion" title="" aria-label="" />
        </Link>
      </div>
    );
  }
}
