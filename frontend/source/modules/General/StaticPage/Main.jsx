import React, { Component } from 'react';

import ScrollToTopOnMount from 'shared/ScrollToTopOnMount';

import Error404 from 'modules/Error/Error404';

import * as pages from './Pages'

export default class StaticPage extends Component {
  constructor(props) {
    super(props);
  }

  componentWillReceiveProps(nextProps) {
    if (this.props.match.params.pageName != nextProps.match.params.pageName) {
      window.scrollTo(0, 0);
    }
  }

  render() {
    let pageName = this.props.match.params.pageName.toLowerCase();

    if (pageName in pages) {
      return (
        <div>
          <ScrollToTopOnMount />
          { pages[pageName]() }
        </div>
      );
    }
    return <Error404 />;
  }
}
