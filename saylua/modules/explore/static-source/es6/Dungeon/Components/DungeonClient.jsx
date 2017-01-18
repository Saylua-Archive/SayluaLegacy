import Inferno from "inferno";
import onDomReady from "ondomready";
import Component from "inferno-component";

import * as CanvasUtils from "../Utils/canvas";
import GameRenderer from "../Core/GameRenderer";

// DungeonClient -> Required by Main
// --------------------------------------
// The actual client. This handles input and renders the map.
// Technically, this can and should be a stateless component
// instead of a traditional one.

export default class DungeonClient extends Component {
  constructor(props) {
    super(props);

    this.refs = {};
    this.state = {};
  }


  componentDidMount() {
    // Create a canvas context with Pixi, then initialize a new GameRenderer and pass said context.
    onDomReady(() => {
      // Store client wrapper, canvas wrapper.
      this.clientWrapper = document.querySelectorAll(".dungeon-client-wrapper")[0];
      this.canvasWrapper = this.refs.pixiCanvas;

      // Calculate the height, and width of our canvas from the window size.
      let [renderWidth, renderHeight] = CanvasUtils.calculateSize();

      // Resize container
      this.clientWrapper.style.height = renderHeight + "px";
      this.clientWrapper.style.width = renderWidth + "px";
      this.canvasWrapper.style.height = renderHeight + "px";
      this.canvasWrapper.style.width = renderWidth + "px";

      // Start game, attach renderer to DOM
      this.gameRenderer = new GameRenderer(renderWidth, renderHeight, this.props.store);
      this.refs.pixiCanvas.appendChild(this.gameRenderer.getRenderer());

      // Bind to the window.resize event.
      window.addEventListener("resize", this.handleWindowResize.bind(this));

      // Match keyboard presses to events.
      this.eventListener = window.addEventListener("keydown", this.handleKeyPress.bind(this));

      // Start looping.
      this.animate();
    });
  }


  animate() {
    this.gameRenderer.loop();
    this.frame = requestAnimationFrame(this.animate.bind(this));
  }


  handleKeyPress(event, synthetic) {
    synthetic = synthetic ? synthetic : false;

    let key, keyName;

    if (synthetic === false && event !== undefined) {
      key = event.keyCode;

      // Key map. Time to pull out the dreaded switch statement.
      switch(key) {
        case 13: // Enter key
          keyName = "enter";
          break;
        case 32: // Space bar
          keyName = "space";
          break;
        case 38:
        case 87: // W, up arrow
          keyName = "up";
          break;
        case 40:
        case 83: // S, down arrow
          keyName = "down";
          break;
        case 37:
        case 65: // A, left arrow
          keyName = "left";
          break;
        case 39:
        case 68: // D, right arrow
          keyName = "right";
          break;
        case 77: // M Key
          keyName = "minimap";
          break;
        default:
          // We are not capturing the key.
          return;
      }
    } else {
      keyName = "synthetic";
    }

    // Frame-time debug timer
    window.framet0 = performance.now();

    let movementKeys = ["up", "down", "left", "right"];

    if (movementKeys.indexOf(keyName) !== -1) {
      // If we've gotten this far, prevent default behavior.
      event.preventDefault();

      this.props.store.dispatch({
        'type': "MOVE_PLAYER",
        'direction': keyName
      });
    }

    if (keyName === "minimap") {
      // If we've gotten this far, prevent default behavior.
      event.preventDefault();

      this.props.store.dispatch({
        'type': "TOGGLE_MINIMAP"
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
      <div className="dungeon-wrapper" ref={(node) => this.refs.pixiCanvas = node} >
      </div>
    );
  }
}
