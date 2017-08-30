import React, { Component } from 'react';

// The main Saylua layout component.
export default class Footer extends Component {
  constructor(props) {
    super(props);
  }

  componentDidMount() {
    setInterval(this.render, 1000);
  }

  render() {
    let date = new Date();
    return (
      <span>
        <i className="fa fa-clock-o" aria-hidden="true"></i>
        { ' ' + date.toUTCString() }
      </span>
    );
  }
}
