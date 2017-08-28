import Inferno from 'inferno';
import Component from 'inferno-component';
import './Header.scss';

export default class Header extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div id="header" className="header">
        <a id="logo" href="/" className="logo"><img id="logo-image" src="/static/img/logo.png" alt="Saylua" title="Saylua" /></a>
      </div>
    );
  }
}
