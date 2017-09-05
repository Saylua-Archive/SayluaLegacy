import React, { Component } from 'react';

import './Notification.scss';

export default class Notification extends Component {
  constructor(props) {
    super(props);
  }

  close(e) {
    e.preventDefault();

    let notification = e.target.parentElement;

    notification.classList.add('notification-fadeup');

    setTimeout(function() {
      notification.parentElement.removeChild(notification);
    }
  }

  render() {
    let message = this.props.message || "Test Message";
    return (
      <div class="notification">
        { message }
        <a class="close-button" href="#" title="close"
          onClick={ this.close.bind(this) }>&#x00d7;</a>
      </div>
    );
  }
}
