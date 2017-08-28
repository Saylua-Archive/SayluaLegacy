import Inferno from 'inferno';
import Saylua from 'shared/Saylua/Saylua';

import { Router, Route, IndexRoute } from 'inferno-router';
import createBrowserHistory from 'history/createBrowserHistory';

import Newspaper from 'modules/General/Newspaper/Newspaper';
import Page from 'modules/General/StaticPage/StaticPage';

import Error404 from 'modules/Error/Error404';


const browserHistory = createBrowserHistory();

const routes = (
  <Router history={ browserHistory }>
    <Route path="/">
      <Saylua title="Home">
        <div>Hello World</div>
      </Saylua>
    </Route>
    <Route path="/page/:page">
      <Page pageName="about" />
    </Route>
    <Route path="/news">
      <Newspaper />
    </Route>
    <Route path="*">
      404
    </Route>
  </Router>
);

Inferno.render(routes, document.getElementById('app'));
