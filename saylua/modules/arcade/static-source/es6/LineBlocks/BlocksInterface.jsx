import Inferno from "inferno";
import Component from "inferno-component";
import BlockGrid from "./BlockGrid";

// The overall game interface for tetris.
export default class BlocksInterface extends Component {
  constructor(props) {
    super(props);
  }

  componentWillMount() {
    // Make sure that when our model updates, we do too.
    this.props.model.bindComponent(this);

    // Match keyboard presses to events.
    this.eventListener = window.addEventListener("keydown", this.handleKeydown.bind(this));
    this.eventListener = window.addEventListener("keyup", this.handleKeyup.bind(this));
  }

  handleKeydown(event) {
    if (!event) return;
    let tag = event.target.tagName.toLowerCase();

    //  Make sure keys can still be inputted if a form is focused.
    if (tag == 'input' || tag == 'textarea') return;

    let key = event.keyCode;

    switch(key) {
      case 13: // Enter
      case 80: // P
        this.props.model.pause();
        break;
      case 32: // Space
        this.props.model.drop();
        break;
      case 38: // Up
      case 87: // W
        this.props.model.rotate();
        break;
      case 40: // Down
      case 83: // S
        this.props.model.speedUp();
        break;
      case 37: // Left
      case 65: // A
        this.props.model.moveLeft();
        break;
      case 39: // Right
      case 68: // D
        this.props.model.moveRight();
        break;
      default:
        return;
    }

    event.preventDefault();
  }

  handleKeyup(event) {
    if (!event) return;
    let tag = event.target.tagName.toLowerCase();
    if (tag == 'input' || tag == 'textarea') return;

    let key = event.keyCode;
    switch(key) {
      case 40: // Down
      case 83: // S
        this.props.model.speedDown();
        break;
      default:
        return;
    }
    event.preventDefault();
  }

  render() {
    let model = this.props.model;
    let overlay = '';
    if (model.gameOver) {
      overlay = <div className='blocks-overlay'>
        <span className='blocks-big-text'>Game Over</span>
        <br />Score: { model.score }
        <br /><span className='blocks-small-text'>
          You earned { model.score } Cloud Coins!</span>
        <br /><span className='blocks-try-again'>Try again?</span>
      </div>;
    } else if (model.paused) {
      overlay = <div className='blocks-overlay'>
        <span className='blocks-big-text'>Paused</span>
      </div>;
    }

    return (
      <div className='blocks-outer-container'>
        { overlay }
        <div className='blocks-container'>
          <div className='blocks-info'>
            <div className='blocks-next-piece'>
              <BlockGrid matrix={ model.nextPiece } />
            </div>
            <div className='blocks-score'>
              Score: { model.score }
            </div>
            <div className='blocks-controls'>
              &larr;&rarr; - Move piece
              <br />&uarr;- Rotate piece
              <br />&darr; - Speedup
              <br />Space - Drop piece
              <br />Enter/P - Pause
            </div>
          </div>
          <BlockGrid className='blocks-grid' matrix={ model.gameMatrix } />
        </div>
      </div>
    );
  }
}
