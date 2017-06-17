import Inferno from "inferno";
import Component from "inferno-component";

export default class Inventory extends Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  componentWillMount() {
    // Make sure that when our model updates, we do too.
    this.props.model.bindComponent(this);
  }

  render() {
    let model = this.props.model;
    let items = model.items.map(function(item, i) {
      return (
        <div class="grid-element">
          <span class="link" onclick={ model.setIndex.bind(model, i) }>
            <img src={ item.image_url } className="item" alt={ item.name }
              title={ item.name } aria-label={ item.name } />
            <span>{ item.name }</span>
          </span>
          <small>Count: { item.count }</small>
        </div>
      );
    });
    let pagination = <div className="pagination"></div>;
    return (
      <div>
        <div className="inventory-categories">
        </div>
        <div className="center">
          { pagination }
        </div>
        <div class="grid-container">
          { items }
        </div>
        <div className="center">
          { pagination }
        </div>
      </div>
    );
  }
}
