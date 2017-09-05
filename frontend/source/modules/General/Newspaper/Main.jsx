import React, { Component } from 'react';

import ScrollToTopOnMount from 'shared/ScrollToTopOnMount';

import SayluaView from 'shared/SayluaView';

import './Newspaper.scss';

export default class Newspaper extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <SayluaView title="The Sayluan Gazette">
        <ScrollToTopOnMount />
        <h1 className="news-header">The Sayluan Gazette</h1>
        <div className="news-navigation">
          <a href="/news/">Headlines</a> / <a href="/news/puzzle/">Daily Puzzle</a>
        </div>
        <div className="newspaper-body">
          <div className="newspaper-main">
          </div>
          <div className="newspaper-side">
          </div>
        </div>
      </SayluaView>
    );
  }
}
