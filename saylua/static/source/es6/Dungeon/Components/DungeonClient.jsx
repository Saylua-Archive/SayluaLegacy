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
      "domLoaded": false
    };
  }

  onComponentWillMount() {
    // Make sure that when our model updates, we do too.
    this.props.model.bindComponent(this);

    // Match keyboard presses to events.
    this.state.eventListener = window.addEventListener("keydown", this.handleKeyPress);

    // In the EXTREMELY rare (probably impossible in real-world conditions)
    // event that we get this far before the DOM has loaded, wait for it to complete
    // so that the entity renderer doesn't have issues.
    document.addEventListener("DOMContentLoaded", (event) => {
      this.setState({ "domLoaded": true });
    });
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

    this.props.model.mutate({action: direction});
  }

  getMap(tileLayer, entityLayer, tileSet, entitySet) {
    // First, we generate our tile layer
    let tileMap = tileLayer.map((row, y) => {
      let cells = row.map((cell, x) => {
        let cellID = tileSet.filter((e) => e.id === cell);
        return (
          <span className={ `cell-${cellID} cell-{x}-{y}` } />
        );
      });

      return (
        <div className="cell-row">
          { cells }
        </div>
      );
    });

    // Now we use our entity layer, along with our generated
    // coord classes to inject entities.
    for (let entity of entityLayer) {
      let content = document.createElement("span");
      content.className = `entity-${entity.parent}`;

      let element = tileMap.dom.querySelectorAll(`cell-${entity.location.x}-${entity.location.y}`)[0];
      element.appendChild(content);
    }

    return tileMap;
  }

  render() {
    let model = this.props.model;
    let map = (this.state.domLoaded) ? this.getMap(model.tileLayer, model.entityLayer, model.tileSet, model.entitySet) : false;

    return (
      <div className="content-wrapper">
        <div className='dungeon-map'>{ map }</div>
      </div>
    );
  }
}