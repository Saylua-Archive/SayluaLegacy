import Inferno from 'inferno';
import Saylua from './components/layout/Saylua';

import { Router, Route, IndexRoute } from 'inferno-router';
import createBrowserHistory from 'history/createBrowserHistory';

import Newspaper from './components/modules/General/Newspaper/Newspaper';
import Page from './components/modules/General/StaticPage/StaticPage';

import { Error404} from './components/error/404';


const browserHistory = createBrowserHistory();

const routes = (
  <Router history={ browserHistory }>
    <IndexRoute>
      <Saylua>
        Hello World
      </Saylua>
    </IndexRoute>
    <Route path="/page/:page">
      <Page pageName="about" />
    </Route>
    <Route path="/news">
      <Newspaper />
    </Route>
    <Route path="*" component={ Error404 } />
  </Router>
);

Inferno.render(routes, document.getElementById('app'));
