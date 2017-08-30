import React, { Component } from 'react';

import Error404 from 'modules/Error/Error404';

import * as pages from './Pages'

export default class StaticPage extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    let pageName = this.props.match.params.pageName.toLowerCase();
    if (pageName in pages) {
      return pages[pageName]();
    }
    return <Error404 />;
  }
}
