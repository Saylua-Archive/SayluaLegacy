import Inferno from 'inferno';
import Component from 'inferno-component';
import './Saylua.scss';

import Navbar from './Navbar/Navbar';

// The main Saylua layout component.
export default class Saylua extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div>
        <div id="banner" className="banner">
          <a id="logo" href="/" className="logo"><img id="logo-image" src="/static/img/logo.png" alt="Saylua" title="Saylua" /></a>
        </div>
        <Navbar />
      </div>
    );
  }
}
