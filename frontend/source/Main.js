import React from 'react';
import ReactDOM from 'react-dom';

import { Provider } from 'react-redux';
import { createStore } from 'redux';

import sayluaApp from 'services/reducers';

import { BrowserRouter, Route, Switch } from 'react-router-dom';

import SayluaView from 'shared/SayluaView';

import Newspaper from 'modules/General/Newspaper';
import StaticPage from 'modules/General/StaticPage';
import Login from 'modules/Users/Login';

import Error404 from 'modules/Error/Error404';


const Root = ({ store }) => (
  <Provider store={ store }>
    <BrowserRouter>
      <Switch>
        <Route path="/home">
          <SayluaView title="Home">
            Hello world
          </SayluaView>
        </Route>
        <Route path="/login" component={ Login } />
        <Route path="/page/:pageName" component={ StaticPage } />
        <Route path="/news" component={ Newspaper} />
        <Route path="*" component={ Error404 } />
      </Switch>
    </BrowserRouter>
  </Provider>
);

let store = createStore(sayluaApp);

ReactDOM.render(<Root store={ store } />, document.getElementById('app'));