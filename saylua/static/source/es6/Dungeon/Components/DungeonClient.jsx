import Inferno from "inferno";
import Component from "inferno-component";

// DungeonClient -> Required by Main
// --------------------------------------
// The actual client. This handles input and renders the map.
// Technically, this can and should be a stateless component
// instead of a traditional one.
//
// Address that if performance ever becomes a concern.

// Fisher-Price's My-First-React notes
// --------------------------------------
// Generally, in a component, I write functions in the following order.
// 1. Constructor
// 2. Lifecycle functions
//    https://facebook.github.io/react/docs/react-component.html#the-component-lifecycle
// 3. Internal functions that are only called by other functions.
// 4. Functions that handle user input.
// 5. Functions that generate DOM elements from data.
//    (In 90% of cases these should not exist, and indicate you should write a new component)
// 6. The actual render() function
//
// The name of the game is to keep your functions as pure as possible, and your components minimal.
// - You should have little to no logic in your render() call.
// - Avoid having components manage their own state, leave that to the component at the top of the food chain.
//   Data in, data out is the mantra.
// - With the above said, do not be afraid to break your mega-component into multiple
//   smaller mega-components with multiple mount points.

export default class DungeonClient extends Component {
  constructor(props) {
    super(props);

    this.state = {
      "domLoaded": true
    };
  }

  componentWillMount() {
    // Make sure that when our model updates, we do too.
    this.props.model.bindComponent(this);

    // Match keyboard presses to events.
    this.state.eventListener = window.addEventListener("keydown", this.handleKeyPress.bind(this));
  }

  handleKeyPress(event) {
    let key = event.keyCode;

    // Default to "move" until more interactions are possible.
    let action = "move";
    let direction;

    // Key map. Time to pull out the dreaded switch statement.
    switch(key) {
      case 38:
      case 87:
        direction = "up";
        break;
      case 40:
      case 83:
        direction = "down";
        break;
      case 37:
      case 65:
        direction = "left";
        break;
      case 39:
      case 68:
        direction = "right";
        break;
      default:
        // We are not capturing the key.
        return;
    }

    // If we've gotten this far, prevent default behavior.
    event.preventDefault();
    this.props.model.mutate({
      'action': action,
      'data': direction
    });
  }

  getMap(tileLayer, entityLayer, tileSet, entitySet) {
    // First, we create a lookup table for entities so that we
    // can insert entities in linear time rather than exponential.
    //
    // This is almost definitely still far more expensive than just injecting them directly.
    // More research necessary to figure out how to do injection properly.
    // Starting point: 'ref (1.0.0) or onAttached (0.7.x) for callback when node is attached first parameter is the node'

    let entityLookupTable = [];

    for (let entity of entityLayer) {
      let content = (<span className={ `entity entity-${entity.parent}` } />);

      let x = entity.location.x;
      let y = entity.location.y;

      entityLookupTable[y] = entityLookupTable[y] || [];
      entityLookupTable[y][x] = entityLookupTable[y][x] || [];

      entityLookupTable[y][x].push(content);
    }

    // Then, we generate our tile layer
    let tileMap = tileLayer.map((row, y) => {
      let cells = row.map((cell, x) => {
        let entities = false;
        let cellSeen = (Object.keys(cell).length > 0);
        let cellID = cellSeen ? cell.tile : 'unseen';
        let classes = ['cell', `cell-${cellID}`, `cell-${x}-${y}`];

        if (cellSeen) {
          if (cell.meta.visible === false) {
            // This cell has been seen before, and is now hidden.
            // Cells that are still undiscovered will not have meta.visible set at all.
            classes.push('cell-hidden');
          }

          if (entityLookupTable[y] !== undefined) {
            if (entityLookupTable[y][x] !== undefined) {
              entities = entityLookupTable[y][x];
            }
          }
        }

        return (
          <span className={ classes.join(' ') } >{ entities }</span>
        );
      });

      return (
        <div className={`cell-row cell-row-${y}`}>
          { cells }
        </div>
      );
    });

    return tileMap;
  }

  render() {
    let model = this.props.model;
    let map = false;

    if (this.state.domLoaded) {
      map = this.getMap(
        model.get('tileLayer'),
        model.get('entityLayer'),
        model.get('tileSet'),
        model.get('entitySet')
      );
    }

    return (
      <div className="dungeon-wrapper">
        <div className='dungeon-map'>{ map }</div>
      </div>
    );
  }
}
