import React from 'react';
import ReactDOM from 'react-dom';

import Saylua from 'shared/Saylua/Saylua';

import { Router, Route } from 'react-router';
import createBrowserHistory from 'history/createBrowserHistory';

import Newspaper from 'modules/General/Newspaper/Newspaper';
import StaticPage from 'modules/General/StaticPage/StaticPage';

import Error404 from 'modules/Error/Error404';


const browserHistory = createBrowserHistory();

const routes = (
  <Router history={ browserHistory }>
    <Route path="/home" component={ Saylua } title="Home">
      <div>Hello world</div>
    </Route>
    <Route path="/page/:page" component={ StaticPage } pageName="about" />
    <Route path="/news" component={ Newspaper} />
    <Route path="*" component={ Error404 } />
  </Router>
);

ReactDOM.render(routes, document.getElementById('app'));
