import Inferno from "inferno";
import Component from "inferno-component";

import {formatNumber} from 'Utils';


export default class ItemModal extends Component {
  constructor(props) {
    super(props);
  }

  close() {
    this.props.closed = true;

    let onClose = this.props.onClose;
    if (onClose) {
      onClose();
    }
  }

  open() {
    this.props.closed = false;
  }

  render() {
    let item = this.props.item;
    let closedClass = this.props.closed ? ' closed' : '';
    let closeFunction = this.close.bind(this);
    // Make sure not to close when you click on children of the overlay.
    let stopPropagation = (e) => {
      e.stopPropagation();
    };
    return (
      <div className={ "modal-overlay" + closedClass } onClick={ closeFunction }>
        <div className="modal" onClick={ stopPropagation }>
          <div className="close" onClick={ closeFunction }>
            &times;
          </div>
          <img src={ item.image_url } className="item" alt={ item.name }
            title={ item.name } aria-label={ item.name } />
          <p className="center">Count: { formatNumber(item.count) }</p>
          <p className="center">Buyback Price: { formatNumber(item.buyback_price) } Cloud Coins</p>
          <p className="center">{ item.description }</p>
        </div>
      </div>
    );
  }
}
