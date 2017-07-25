import Inferno from 'inferno';
import Component from 'inferno-component';
import './Dropdown.scss';

export default class Dropdown extends Component {
  constructor(props) {
    super(props);
  }

  componentDidMount() {
    document.body.addEventListener('click', closeOnOutsideClick);
    function closeOnOutsideClick (e) {
      let target = e.target;
      if (!menu.contains(target)) {
        this.unfocus();
      }
    }
  }

  focus() {
    e.preventDefault();
    if (this.props.active) {
      // Clicking on a selected icon removes the menu
      this.unfocus();
    } else {
      this.props.active = true;
    }
  }

  unfocus() {
    this.props.active = false;
  }

  render() {
    let icon = 'fa-globe';
    let name = 'Site';
    let title = 'General Saylua Stuff';
    let active = this.props.active;
    return (
      <div className="navbar-block navbar-main-links">
        <a className="navbar-link" onclick={ this.focus.bind(this) }>
          <i className={"fa fa-fw " + icon } aria-hidden="true" title={ name }></i>
          <label>{ name }</label>
        </a>
        <div className="dropdown-menu menu">
          <h3>{ title }</h3>

        </div>
      </div>
    );
  }
}
