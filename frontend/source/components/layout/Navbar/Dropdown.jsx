import Inferno from 'inferno';
import Component from 'inferno-component';
import './Dropdown.scss';

export default class Dropdown extends Component {
  constructor(props) {
    super(props);

    this.state = {
      opened: false,
    };
  }

  componentDidMount() {
    document.body.addEventListener('click', closeOnOutsideClick);
    function closeOnOutsideClick (e) {
      // TODO
    }
  }

  open() {
    this.setState({
      opened: true,
    });
    let onOpen = this.props.onOpen;
    if (onOpen) {
      onOpen();
    }
  }

  close() {
    this.setState({
      opened: false,
    });
  }

  render() {
    let icon = 'fa-globe';
    let name = 'Site';
    let title = 'General Saylua Stuff';
    let active = this.state.opened;

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
          <i className={ "fa fa-fw " + icon } aria-hidden="true" title={ name }></i>
          <label>{ name }</label>
        </a>
        <div className={ (active ? "open " : "") +  "dropdown-menu menu" }>
          <h3>{ title }</h3>
        </div>
      </div>
    );
  }
}

Dropdown.defaultProps = {
  onOpen: null,
  onClose: null,
};
