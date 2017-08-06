import Inferno from 'inferno';
import Component from 'inferno-component';

import Saylua from '../../../layout/Saylua';

import * as pages from './Pages'

export default class StaticPage extends Component {
  constructor(props) {
    super(props);
  }

  render() {    
    let pageName = this.props.pageName.toLowerCase();
    if (pageName in pages) {
      return pages[pageName]();
    }
    // TODO(tiff): replace this with a 404 component.
    return "Not Found";
  }
}
