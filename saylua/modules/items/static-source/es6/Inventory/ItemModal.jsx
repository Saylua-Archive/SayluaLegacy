import Inferno from "inferno";
import Component from "inferno-component";

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
    let itemName = this.props.itemName;
    let itemImage = this.props.itemImage;
    let itemDescription = this.props.itemDescription;
    let closedClass = this.state.closed ? ' closed' : '';
    return (
      <div className={ "modal-overlay" + closedClass } onClick={ this.close() }>
        <div className="modal">
          <div className="close" onClick={ this.close() }>
            &times;
          </div>
          <img src={ itemImage } className="item" alt={ itemName }
            title={ itemName } aria-label={ itemName } />
          { itemDescription }
        </div>
      </div>
    );
  }
}
