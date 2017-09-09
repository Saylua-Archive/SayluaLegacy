import React, { Component } from 'react';

import { Route, Switch } from 'react-router-dom';

import NewspaperTemplate from './NewspaperTemplate';

import Saydoku from './Saydoku';

export default class Newspaper extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <Switch>
        <Route path="/news/puzzle" component={ Saydoku } />
        <Route path="/news">
          <NewspaperTemplate>
            Hello world
          </NewspaperTemplate>
        </Route>
      </Switch>
    );
  }
}
