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
    let item = this.props.item;
    let closedClass = this.state.closed ? ' closed' : '';
    let onClose = this.props.onClose;
    if (!onClose) {
      onClose = this.close.bind(this);
    }
    return (
      <div className={ "modal-overlay" + closedClass } onClick={ onClose }>
        <div className="modal">
          <div className="close" onClick={ onClose }>
            &times;
          </div>
          <img src={ item.image_url } className="item" alt={ item.name }
            title={ item.name } aria-label={ item.name } />
          { item.description }
        </div>
      </div>
    );
  }
}
