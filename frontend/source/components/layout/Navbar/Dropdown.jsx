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
    let icon = this.props.icon;
    let name = this.props.name;
    let title = this.props.title;
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
      <div className={ (active ? "active " : "") + "navbar-block navbar-main-links" }
          ref={ root => { this.root = root; } }>
        <a className="navbar-link" onClick={ clickLink }>
          <i className={ "fa fa-fw " + icon } aria-hidden="true" title={ name }></i>
          <label>{ name }</label>
        </a>
        <div className="dropdown-menu menu">
          <h3>{ title }</h3>
          <a href="/"><img src="/static/img/icons/house.png" /> My House</a>
          <a href="/news/"><img src="/static/img/icons/newspaper.png" /> Saylua News</a>
          <a href="/inventory/"><img src="/static/img/icons/box.png" /> My Inventory</a>
        </div>
      </div>
    );
  }
}

Dropdown.defaultProps = {
  onOpen: null,
  onClose: null,
};
