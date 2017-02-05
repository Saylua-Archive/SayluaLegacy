// DebugTools -> Required by Main
// --------------------------------------
// Does what it says on the tin.

import Inferno from "inferno";
import Component from "inferno-component";

import DebugGeneral from "./Debug/General";
import DebugEditor from "./Debug/Editor";
import DebugSummoner from "./Debug/Summoner";


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

    this.state = {
      'activeSection': 'general'
    };
  }


  debugEnableFOV() {
    console.log("Toggled!");
    this.store.dispatch({
      'type': 'DEBUG_TOGGLE_FOV'
    });
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


  selectSection(section, event) {
    event.preventDefault();
    this.setState({
      'activeSection': section
    });
  }


  getActiveSection() {
    if (this.state.activeSection === 'general') {
      return (
        <DebugGeneral
          store={ this.store }
          debugEnableFOV={ this.debugEnableFOV.bind(this) }
          debugRevealMap={ this.debugRevealMap.bind(this) }
          debugRegenerateDungeon={ this.debugRegenerateDungeon.bind(this) }
        />
      );
    }

    else if (this.state.activeSection === 'editor') {
      return (
        <DebugEditor store={ this.store } />
      );
    }

    else if (this.state.activeSection === 'summoner') {
      return (
        <DebugSummoner store={ this.store } />
      );
    }
  }


  generateMenuItems() {
    let items = [
      'general',
      'editor',
      'summoner'
    ];

    let menuItems = items.map((item) => {
      let classes = [];
      let properName = `${ item[0].toUpperCase() }${ item.slice(1)}`;

      classes.push(`item-${item}`);

      if (this.state.activeSection === item) {
        classes.push('active');
      }

      return (
        <li className={ classes.join(' ') } onClick={ this.selectSection.bind(this, item) }>
          <div className="icon"></div>
          <span>{ properName }</span>
        </li>
      );
    });

    return menuItems;
  }


  render() {
    let selectedSection = this.getActiveSection();
    let items = this.generateMenuItems();

    return (
      <div className="dungeon-debug-tools">
        <div className="debug-menu">
          <ul>
            { items }
          </ul>
        </div>
        <div className="debug-section">
          { selectedSection }
        </div>
      </div>
    );
  }
}
