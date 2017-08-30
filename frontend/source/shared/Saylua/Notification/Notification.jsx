import React, { Component } from 'react';

import './Notification.scss';

export default class Notification extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    let message = this.props.message || "Test Message";
    return (
      <div class="notification">
        { message }
        <a class="close-button" href="#" title="close">&#x00d7;</a>
      </div>
    );
  }
}
