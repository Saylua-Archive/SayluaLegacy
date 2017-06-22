import Inferno from "inferno";
import Component from "inferno-component";

import {formatNumber} from 'Utils';


export default class ItemModal extends Component {
  constructor(props) {
    super(props);
    this.state = {
      closed: this.props.closed
    };
  }

  close() {
    this.setState({closed: true});
  }

  open() {
    this.setState({closed: false});
  }

  render() {
    let item = this.props.item;
    let closedClass = this.state.closed ? ' closed' : '';
    let onClose = this.props.onClose;
    if (!onClose) {
      onClose = this.close.bind(this);
    }
    // Make sure not to close when you click on children of the overlay.
    let stopPropagation = (e) => {
      e.stopPropagation();
    }
    return (
      <div className={ "modal-overlay" + closedClass } onClick={ onClose }>
        <div className="modal" onClick={ stopPropagation }>
          <div className="close" onClick={ onClose }>
            &times;
          </div>
          <img src={ item.image_url } className="item" alt={ item.name }
            title={ item.name } aria-label={ item.name } />
          <p className="center">Count: { formatNumber(item.count) }</p>
          <p className="center">Autosale Price: { formatNumber(item.price) } Cloud Coins</p>
          <p className="center">{ item.description }</p>
        </div>
      </div>
    );
  }
}
