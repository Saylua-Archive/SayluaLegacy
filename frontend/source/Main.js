import React from 'react';
import ReactDOM from 'react-dom';

import Saylua from 'shared/Saylua/Saylua';

import { BrowserRouter, Route, Switch } from 'react-router-dom';

import Newspaper from 'modules/General/Newspaper/Newspaper';
import StaticPage from 'modules/General/StaticPage/StaticPage';

import Error404 from 'modules/Error/Error404';


const routes = (
  <BrowserRouter>
    <Switch>
      <Route path="/home">
        <Saylua title="Home">
          Hello world
        </Saylua>
      </Route>
      <Route path="/page/:pageName" component={ StaticPage } />
      <Route path="/news" component={ Newspaper} />
      <Route path="*" component={ Error404 } />
    </Switch>
  </BrowserRouter>
);

ReactDOM.render(routes, document.getElementById('app'));
