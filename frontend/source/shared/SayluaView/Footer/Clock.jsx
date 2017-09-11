import React, { Component } from 'react';

import moment from 'moment';

// The main Saylua layout component.
export default class Footer extends Component {
  constructor(props) {
    super(props);
  }

  componentDidMount() {
    setInterval(() => {
      this.forceUpdate();
    }, 1000);
  }

  render() {
    let date = moment();
    return (
      <span>
        <i className="fa fa-clock-o" aria-hidden="true"></i>
        { ' ' + date.format('ddd, MMM DD, Y hh:mm:ss A') + ' SMT' }
      </span>
    );
  }
}
