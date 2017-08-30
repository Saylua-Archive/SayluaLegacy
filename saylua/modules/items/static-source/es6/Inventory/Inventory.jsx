import Inferno from "inferno";
import Component from "inferno-component";

import ItemModal from "./ItemModal";
import Pagination from "Pagination";

import {formatNumber} from 'Utils';

export default class Inventory extends Component {
  constructor(props) {
    super(props);
    this.state = {};

    window.addEventListener('keydown', (e) => {
      e = e || window.event;
      let model = this.props.model;
      if (!model.getItem()) return;
      if (e.keyCode == '37') {
        // left arrow
        model.prevItem();
      }
      else if (e.keyCode == '39') {
        // right arrow
        model.nextItem();
      }
    });
  }

  componentWillMount() {
    // Make sure that when our model updates, we do too.
    this.props.model.bindComponent(this);
  }

  render() {
    let model = this.props.model;

    let categories = model.categories.map(function(category) {
      return (
        <a className="subtle-button" onClick={ model.setCategory.bind(model, category.id) } key={ category.id }>
          { category.name }
        </a>
      );
    });

    let body = model.items.map(function(item, i) {
      let gridClass = "grid-element";
      if (i == model.index) {
        gridClass += " selected";
      }
      return (
        <div className={ gridClass } key={ item.name }>
          <span className="link" onClick={ model.setIndex.bind(model, i) }>
            <img src={ item.image_url } className="item" alt={ item.name }
              title={ item.name } aria-label={ item.name } />
            <span>{ item.name }</span>
          </span>
          <small>Count: { formatNumber(item.count) }</small>
        </div>
      );
    });

    if (!model.fetched) {
      body = <div className="loader center"></div>;
    }

    let pagination = <Pagination currentPage={ model.currentPage }
      pageCount={ model.pageCount } onPageChange={ model.setCurrentPage.bind(model) } />;
    let itemModal = null;
    let item = model.getItem();
    if (item) {
      let onModalClose = () => {
        model.setIndex(-1);
      };
      itemModal = <ItemModal item={ item } companion={ model.companion }
        onClose={ onModalClose } />;
    }
    return (
      <div>
        <div className="inventory-categories center">
          { categories }
        </div>
        { pagination }
        <div className="grid-container">
          { body }
        </div>
        { pagination }
        { itemModal }
      </div>
    );
  }
}
