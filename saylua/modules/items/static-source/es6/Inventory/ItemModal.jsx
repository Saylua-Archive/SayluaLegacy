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
    return (
      <div className={ "modal-overlay" + closedClass } onClick={ this.close.bind(this) }>
        <div className="modal">
          <div className="close" onClick={ this.close.bind(this) }>
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
