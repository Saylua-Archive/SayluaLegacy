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
    <Route path="/" title="Home">
      <Saylua title="Home">Hello world</Saylua>
    </Route>
  </Router>
);

/*
<Route path="/page/:page" component={ StaticPage } pageName="about" />
<Route path="/news" component={ Newspaper} />
<Route path="*" component={ Error404 } />
*/

ReactDOM.render(routes, document.getElementById('app'));
