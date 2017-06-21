import Inferno from "inferno";
import Component from "inferno-component";

import ItemModal from "./ItemModal";
import Pagination from "./Pagination";

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
    let pagination = <Pagination className="center" currentPage={ model.currentPage }
        pageCount={ model.pageCount } onPageChange={ model.setCurrentPage.bind(model) } />;
    let itemModal = null;
    let item = model.getItem();
    if (item) {
      let onModalClose = () => {
        model.setIndex(-1);
      };
      itemModal = <ItemModal item={ item } onClose={ onModalClose } />
    }
    return (
      <div>
        <div className="inventory-categories">
        </div>
        { pagination }
        <div class="grid-container">
          { items }
        </div>
        { pagination }
        { itemModal }
      </div>
    );
  }
}
