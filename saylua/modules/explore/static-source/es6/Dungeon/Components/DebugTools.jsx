import Inferno from "inferno";
import Component from "inferno-component";


export default class DebugTools extends Component {
  constructor(props) {
    super(props);

    // Initialize the gameState from our store.
    this.store = this.props.store;
    this.gameState = this.store.getState();

    // Update our copy of the gamestate when the store updates.
    this.unsubscribe = this.store.subscribe(() => {
      this.gameState = this.store.getState();
    });

    this.state = {};
  }

  debugRegenerateDungeon() {
    this.store.dispatch({
      'type': 'DEBUG_REGENERATE_DUNGEON'
    });
  }

  debugRevealMap() {
    this.store.dispatch({
      'type': 'DEBUG_REVEAL_MAP'
    });
  }

  render() {
    return (
      <div className="dungeon-debug-tools">
        <p>IT'S DEBUGGING TIME, BABY</p> <br />
        <button onClick={ this.debugRegenerateDungeon.bind(this) }>Regenerate Dungeon</button>
        <button onClick={ this.debugRevealMap.bind(this) }>Reveal Dungeon</button>
      </div>
    );
  }
}
