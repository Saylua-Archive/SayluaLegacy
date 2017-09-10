import React, { Component } from 'react';

import { Route, Switch, Link } from 'react-router-dom';

import { expandedRelativeTime } from 'utils';

import NewspaperTemplate from './NewspaperTemplate';

import Saydoku from './Saydoku';

export default class Newspaper extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    let newsSidebar = (
      <div>
        <h3>Random Pet</h3>
        <div className="newspaper-side-box center">
          <img src="/static/img/pets/loxi/common.png" />
        </div>
      </div>
    );

    return (
      <Switch>
        <Route path="/news/puzzle" component={ Saydoku } />
        <Route path="/news">
          <NewspaperTemplate sidebar={ newsSidebar }>
            <div className="news-post-container">
              <h2>
                <img src="/static/img/items/materials/amber.png" className="news-post-avatar" />
                News Title
              </h2>
              <div className="news-post-attribution">by <Link to="/user/">Tiff</Link> on { expandedRelativeTime(new Date()) }</div>
              <article>
                News body
                <Link to="/forums/thread/">View Comments (0)</Link>
              </article>
            </div>
          </NewspaperTemplate>
        </Route>
      </Switch>
    );
  }
}
