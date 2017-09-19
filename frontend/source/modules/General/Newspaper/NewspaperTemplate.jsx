import React, { Component } from 'react';

import { Link } from 'react-router-dom';

import SayluaView from 'shared/SayluaView';

import './Newspaper.scss';

export default class NewspaperTemplate extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <SayluaView title="The Sayluan Gazette">
        <h1 className="news-header">The Sayluan Gazette</h1>
        <div className="news-navigation">
          <Link to="/news/">Headlines</Link> / <Link to="/news/puzzle/">Daily Puzzle</Link>
        </div>
        <div className="newspaper-body">
          <div className="newspaper-main">
            { this.props.children }
          </div>
          <div className="newspaper-side">
            { this.props.sidebar }
          </div>
        </div>
      </SayluaView>
    );
  }
}
