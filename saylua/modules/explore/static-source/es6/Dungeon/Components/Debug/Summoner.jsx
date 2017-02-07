import Reqwest from "reqwest";
import Inferno from "inferno";
import Component from "inferno-component";

import { resolveImage } from "../../Core/graphics";

export default class DebugSummoner extends Component {
  constructor(props) {
    super(props);

    this.state = {
      "entities": [],
      "tiles": [],
      "search": "",
      "searchActive": false,
      "hoveredItem": ""
    };
  }

  componentWillMount() {
    let entities = Reqwest({
      "url": '/explore/api/list_entities',
      "type": 'json',
      "method": 'post'
    });

    let tiles = Reqwest({
      "url": '/explore/api/list_tiles',
      "type": 'json',
      "method": 'post'
    });

    Promise.all([entities, tiles]).then((results) => {
      this.setState({
        "entities": results[0].result,
        "tiles": results[1].result
      });
    });
  }


  handleItemClick(e) {
    let itemID = e.target.dataset['id'];
    let isTile = itemID.startsWith("tile");
    let target;

    if (isTile === true) {
      target = this.state.tiles.filter((tile) => (tile.id == itemID));
      target = target[0];
    } else {
      target = this.state.entities.filter((entity) => (entity.id == itemID));
      target = target[0];
    }

    this.props.debugQueueSummon(target);
  }


  handleItemHover(e) {
    let itemName = e.target.dataset['name'];

    this.setState({
      "hoveredItem": itemName
    });
  }


  handleItemHoverOut(e) {
    this.setState({
      "hoveredItem": ""
    });
  }


  handleSearchChange(e) {
    e.preventDefault();

    let newValue = e.target.value;
    let searchActive = (newValue.trim() !== '');

    this.setState({
      "search": e.target.value,
      "searchActive": searchActive
    });
  }


  generateListItems(iterator) {
    let items = iterator.map((item) => {
      let itemString = `${item.name || 'Unknown'}  :  ${item.id}`;
      let imageURL;

      // Attempt to locate matching image URL
      // default to the debug nil image.
      try {
        imageURL = resolveImage(item.id);
      } catch(e) {
        imageURL = resolveImage('debug_x');
      }

      return (
        <li
          onClick={ this.handleItemClick.bind(this) }
          onMouseEnter={ this.handleItemHover.bind(this) }
          onMouseLeave={ this.handleItemHoverOut.bind(this) }
          data-name={ itemString }
          data-id={ item.id }
        >
          <div className="image-container">
            <img
              src={ imageURL }
              alt={ item.name }
              data-id={ item.id } // We have to define this here too because onClick returns the targeted element directly.
            />
          </div>
        </li>
      );
    });

    return items;
  }


  render() {
    let validEntities = this.state.entities.filter((entity) => {
      if (entity.name === null) {
        return (entity.id.indexOf(this.state.search) >= 0);
      } else {
        return (
          entity.name.indexOf(this.state.search) >= 0 ||
          entity.id.indexOf(this.state.search) >= 0
        );
      }
    });

    let validTiles = this.state.tiles.filter((tile) => {
      if (tile.name === null) {
        return (tile.id.indexOf(this.state.search) >= 0);
      } else {
        return (
          tile.name.indexOf(this.state.search) >= 0 ||
          tile.id.indexOf(this.state.search) >= 0
        );
      }
    });

    let entities = this.generateListItems(validEntities);
    let tiles = this.generateListItems(validTiles);

    let searchTextClasses = ['search-text'];

    if (this.state.searchActive) {
      searchTextClasses.push('active');
    }

    return (
      <div className="section-summoner">
        <div className="summoner-search">
          <span className="hover-item">{ this.state.hoveredItem }</span>
          <span className={ searchTextClasses.join(' ') }>search</span>
          <input
            type="text"
            value={ this.state.search }
            onInput={ this.handleSearchChange.bind(this) }
          />
        </div>
        <div className="summoner-select">
          <div className="select-entities">
            <h4>Entities</h4>
            <ul>
              { entities }
            </ul>
          </div>
          <div className="select-tiles">
            <h4>Tiles</h4>
            <ul>
              { tiles }
            </ul>
          </div>
        </div>
      </div>
    );
  }
}
