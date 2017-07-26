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
        this.close();
      }
    }
  }

  open() {
    this.props.opened = true;
    let onOpen = this.props.onOpen;
    if (onOpen) {
      onOpen();
    }
  }

  close() {
    this.props.opened = false;
  }

  render() {
    let icon = 'fa-globe';
    let name = 'Site';
    let title = 'General Saylua Stuff';
    let active = this.props.opened;

    let clickLink = (e) => {
      e.preventDefault();
      if (active) {
        this.close();
      } else {
        this.open();
      }
    };
    return (
      <div className="navbar-block navbar-main-links">
        <a className="navbar-link" onClick={ clickLink }>
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
