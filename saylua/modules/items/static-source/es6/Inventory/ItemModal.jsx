import Inferno from "inferno";
import Component from "inferno-component";

// Renders an instance of the game matrix.
export default class BlockGrid extends Component {
  constructor(props) {
    super(props);
  }

  close() {
    this.props.closed = true;
  }

  render() {
    let itemName = this.props.itemName;
    let itemImage = this.props.itemImage;
    let itemDescription = this.props.itemDescription;
    let closedClass = this.props.closed ? ' closed' : '';
    return (
      <div className="modal-overlay{ closedClass }" onClick={ this.close() }>
        <div className="modal">
          <div className="close" onClick={ this.close() }>
            &times;
          </div>
          <img src="{ itemImage }" className="item" alt="{ itemName }"
            title="{ itemName }" aria-label="{ itemName }" />
          { itemDescription }
        </div>
      </div>
    );
  }
}
