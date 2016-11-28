import Inferno from "inferno";
import Component from "inferno-component";

import cloneDeep from "lodash.clonedeep";

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
    this.eventListener = window.addEventListener("keydown", this.handleKeyPress.bind(this));
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

  getMap(tileLayer, entityLayer, tileSet, entitySet, radius=8) {
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

    // Then, we generate our map and mini-map simultaneously
    let mapView = [];

    let player = entityLayer[0];

    let p_x = player.location.x;
    let p_y = player.location.y;

    let mapHeight = tileLayer.length;
    let mapWidth = tileLayer[0].length;

    // Define mapView bounds
    // Probably both the best and the worst thing I have written all week.
    // Keeps two points within the bounds of the map, and a minimum distance from each other.

    let a_x, b_x, x_pool;
    x_pool = radius * 2;

    a_x = Math.max(p_x - radius, 0);                                    // console.log(`a_x is ${a_x}`);
    x_pool -= (p_x - a_x);                                              // console.log(`Units left in the pool: is ${x_pool}`);
    b_x = Math.min(p_x + x_pool, mapWidth - 1);                         // console.log(`b_x is ${b_x}`);
    x_pool -= (b_x - p_x);                                              // console.log(`Units left in the pool: is ${x_pool}`);
    a_x = (b_x === mapWidth - 1) ? (a_x - x_pool) : (a_x + x_pool);     // console.log(`Adding ${x_pool} to a_x makes: ${a_x}`);

    let a_y, b_y, y_pool;
    y_pool = radius * 2;

    a_y = Math.max(p_y - radius, 0);
    y_pool -= (p_y - a_y);
    b_y = Math.min(p_y + y_pool, mapHeight - 1);
    y_pool -= (b_y - p_y);
    a_y = (b_y === mapHeight - 1) ? (a_y - y_pool) : (a_y + y_pool);

    let miniMap = tileLayer.map((row, y) => {
      let mapViewRow = [];
      let within_y_bounds = (a_y <= y) && (y <= b_y);

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

        // Generate element
        let el = (
          <span className={ classes.join(' ') } >{ entities }</span>
        );

        // Should we also push a clone of this element to the mapViewRow?
        let within_x_bounds = (a_x <= x) && (x <= b_x);
        if (within_x_bounds && within_y_bounds) {
          // Clone entities with cloneDeep() and add class to prevent diffing issues.
          classes.push("map-view-cell");
          let cloned_entities;

          // Add neighbor information
          if (cellSeen) {
            classes.push(`ordinal-${cell.meta.ordinals}`);
          }

          if (entities !== false) {
            cloned_entities = cloneDeep(entities);
          } else {
            cloned_entities = false;
          }

          let cloned_el = (
            <span className={ classes.join(' ') } >
              { cloned_entities }
            </span>
          );
          mapViewRow.push(cloned_el);
        }

        return el;
      });

      // Should we also push a row to the mapView?
      if (within_y_bounds) {
        mapView.push(
          <div className={`map-view-row cell-row cell-row-${y}`}>
            { mapViewRow }
          </div>
        );
      }

      return (
        <div className={`simple cell-row cell-row-${y}`}>
          { cells }
        </div>
      );
    });

    return [mapView, miniMap];
  }

  render() {
    let model = this.props.model;
    let mapView = false;
    let miniMap = false;

    if (this.state.domLoaded) {
      [mapView, miniMap] = this.getMap(
        model.get('tileLayer'),
        model.get('entityLayer'),
        model.get('tileSet'),
        model.get('entitySet')
      );

      this.props.miniMap.set(miniMap);
    }

    return (
      <div className="dungeon-wrapper">
        <div className='dungeon-map'>
          { mapView }
        </div>
      </div>
    );
  }
}
