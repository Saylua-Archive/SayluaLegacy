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
      'activeSection': 'general',
      "__forceReRender": false
    };
  }

  forceReRender(component) {
    this.setState({
      "__forceReRender": !this.state.__forceReRender
    });
  }


  debugClearCache() {
    localStorage.clear();
  }


  debugToggleOption(name) {
    this.store.dispatch({
      'type': 'DEBUG_TOGGLE_OPTION',
      'name': name
    });

    this.forceReRender();
  }

  debugRegenerateDungeon() {
    this.store.dispatch({
      'type': 'DEBUG_REGENERATE_DUNGEON'
    });

    this.forceReRender();
  }


  debugRevealMap() {
    this.store.dispatch({
      'type': 'DEBUG_REVEAL_MAP'
    });

    this.forceReRender();
  }

  debugQueueSummon(target) {
    this.store.dispatch({
      'type': 'DEBUG_QUEUE_SUMMON',
      'summon': target
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
          debugClearCache={ this.debugClearCache.bind(this) }
          debugToggleOption={ this.debugToggleOption.bind(this) }
          debugRevealMap={ this.debugRevealMap.bind(this) }
          debugRegenerateDungeon={ this.debugRegenerateDungeon.bind(this) }
          __forceReRender={ this.state.__forceReRender }
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
        <DebugSummoner
          store={ this.store }
          debugQueueSummon={ this.debugQueueSummon.bind(this) }
        />
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
