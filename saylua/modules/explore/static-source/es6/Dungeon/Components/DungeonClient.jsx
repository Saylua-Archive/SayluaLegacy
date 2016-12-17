import Inferno from "inferno";
import onDomReady from "ondomready";
import Component from "inferno-component";

import * as CanvasUtils from "../Utils/canvas";
import Game from "../Core/Game";

// DungeonClient -> Required by Main
// --------------------------------------
// The actual client. This handles input and renders the map.
// Technically, this can and should be a stateless component
// instead of a traditional one.

export default class DungeonClient extends Component {
  constructor(props) {
    super(props);

    this.state = {};
  }

  componentDidMount() {
    // Start rendering Pixi canvas once our component has mounted.
    onDomReady(() => {
      // Store client wrapper, canvas wrapper.
      this.clientWrapper = document.querySelectorAll(".dungeon-client-wrapper")[0];
      this.canvasWrapper = this.refs.pixiCanvas;

      // Calculate the height, width of our canvas from the window size.
      let [renderWidth, renderHeight] = CanvasUtils.calculateSize();

      // Resize container
      this.clientWrapper.style.height = renderHeight + "px";
      this.clientWrapper.style.width = renderWidth + "px";
      this.canvasWrapper.style.height = renderHeight + "px";
      this.canvasWrapper.style.width = renderWidth + "px";

      // Start Game, attach renderer to DOM
      this.game = new Game(renderWidth, renderHeight, this.props.store);
      this.refs.pixiCanvas.appendChild(this.game.getRenderer());

      // Bind to the window.resize event.
      window.addEventListener("resize", this.handleWindowResize.bind(this));

      // Match keyboard presses to events.
      this.eventListener = window.addEventListener("keydown", this.handleKeyPress.bind(this));

      // Start looping.
      this.animate();
    });
  }

  animate() {
    this.game.loop();
    this.frame = requestAnimationFrame(this.animate.bind(this));
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

  handleWindowResize(e) {
    let [renderWidth, renderHeight] = CanvasUtils.calculateSize();

    this.clientWrapper.style.height = renderHeight + "px";
    this.clientWrapper.style.width = renderWidth + "px";
    this.canvasWrapper.style.height = renderHeight + "px";
    this.canvasWrapper.style.width = renderWidth + "px";
  }

  render() {
    return (
      <div className="dungeon-wrapper" ref="pixiCanvas">
      </div>
    );
  }
}
