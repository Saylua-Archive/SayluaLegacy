import Inferno from "inferno";
import Component from "inferno-component";

import DungeonMap from "./DungeonMap";

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
      "domLoaded": true,
      "transitioning": false
    };
  }

  componentWillMount() {
    // Make sure that when our model updates, we do too.
    this.props.model.bindComponent(this);

    // Match keyboard presses to events.
    this.eventListener = window.addEventListener("keydown", this.handleKeyPress.bind(this));
  }

  handleForceTransition(event) {
    event.preventDefault();
    this.handleKeyPress(undefined, true);
  }

  handleKeyPress(event, synthetic) {
    synthetic = synthetic ? synthetic : false;

    let key, keyName;

    if (synthetic === false && event !== undefined) {
      key = event.keyCode;

      // Key map. Time to pull out the dreaded switch statement.
      switch(key) {
        case 13:
          keyName = "enter";
          break;
        case 32:
          keyName = "space";
          break;
        case 38:
        case 87:
          keyName = "up";
          break;
        case 40:
        case 83:
          keyName = "down";
          break;
        case 37:
        case 65:
          keyName = "left";
          break;
        case 39:
        case 68:
          keyName = "right";
          break;
        default:
          // We are not capturing the key.
          return;
      }
    } else {
      keyName = "synthetic";
    }

    let movementKeys = ["up", "down", "left", "right"];

    if (movementKeys.indexOf(keyName) !== -1) {
      // If we've gotten this far, prevent default behavior.
      event.preventDefault();

      this.props.model.mutate({
        'action': "move",
        'data': keyName
      });
    }
  }

  render() {
    return (
      <div className="dungeon-wrapper">
        <DungeonMap miniMap={ this.props.miniMap } model={ this.props.model } />
      </div>
    );
  }
}
