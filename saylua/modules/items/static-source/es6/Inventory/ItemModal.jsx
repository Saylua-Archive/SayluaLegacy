import Inferno from "inferno";
import Component from "inferno-component";

import {formatNumber} from 'Utils';
import { getCsrfToken } from "saylua-fetch";


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
    let companion = this.props.companion;
    let closedClass = this.props.closed ? ' closed' : '';
    let closeFunction = this.close.bind(this);
    // Make sure not to close when you click on children of the overlay.
    let stopPropagation = (e) => {
      e.stopPropagation();
    };

    let buybackOptions = [];
    for (let i = 1; i <= item.count; i++) {
      buybackOptions.push(<option value={ i }>Sell { i + " for " + i * item.buyback_price }</option>);
    }

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
          <form method="post" action="/mini/bond/" className="center">
            <input type="hidden" name="mini_id" value={ item.id } />
            <input type="hidden" name="pet_id" value={ companion.id } />
            <input type="hidden" name="csrf_token" value={ getCsrfToken() }/>
            <button>{ "Bond with " + companion.name }</button>
          </form>
          <form method="post" action="/autosale/" className="center">
            <select name="amount">
              { buybackOptions }
            </select>
            <input type="hidden" name="item_id" value={ item.id } />
            <input type="hidden" name="csrf_token" value={ getCsrfToken() }/>
            <button>Sell</button>
          </form>
        </div>
      </div>
    );
  }
}
