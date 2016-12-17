import Inferno from "inferno";
import Component from "inferno-component";

import cloneDeep from "lodash.clonedeep";

export default class DungeonMap extends Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  componentDidMount() {
    // Make sure that when our model updates, we do too.
    this.props.model.bindComponent(this);
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

    [mapView, miniMap] = this.getMap(
      model.get('tileLayer'),
      model.get('entityLayer'),
      model.get('tileSet'),
      model.get('entitySet')
    );

    this.props.miniMap.set(miniMap);

    return (
      <div className='dungeon-map'>
        { mapView }
      </div>
    );
  }
}
