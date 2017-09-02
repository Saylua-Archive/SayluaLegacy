import React, { Component } from 'react';

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
          <a href="">
            <img src="/static/img/avatar/base.png" alt="human avatar" title="'s Avatar'" aria-label="'s Avatar'" />
          </a>
        </div>
        <a href="" className="active-pet-view">
          <img src="/static/img/pets/loxi/common.png" className="active-pet-image" alt="active companion" title="" aria-label="" />
        </a>
      </div>
    );
  }
}
