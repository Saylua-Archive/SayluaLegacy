/* global ace */
/* eslint { "inferno/no-unescaped-entities": 0 } */
// Editor -> Required by DebugTools
// --------------------------------------
// Allows developers to edit entity / tile
// fields and scripts.

import Inferno from "inferno";
import Component from "inferno-component";

import { compileScript } from "../../Core/scripting";
import { injectScript } from "Utils";


// function isTrueObject(o) {
//   return Object.prototype.toString.call(o) === "[object Object]";
// }


export default class DebugEditor extends Component {
  constructor(props) {
    super(props);

    this.store = this.props.store;

    let initialState = this.store.getState();

    this.state = {
      "storeState": initialState,
      "selected": {
        "location": "",
        "content": ""
      },
      "_forceUpdate": false
    };

    this.refs = {};
    this.promise = undefined;
  }


  componentDidMount() {
    // Wait until Ace has loaded, then inject it into our DOM.
    this.promise.then(() => {
      this.editor = ace.edit(this.refs.editor);
      this.editor.setTheme("ace/theme/twilight");
      this.editor.session.setMode("ace/mode/javascript");
      this.editor.setFontSize(20);
    });
  }


  componentWillMount() {
    window.aceEditorLoaded = window.aceEditorLoaded || false;

    if (window.aceEditorLoaded === false) {
      // Store our promise for later
      this.promise = injectScript('https://cdnjs.cloudflare.com/ajax/libs/ace/1.2.6/ace.js');

      // Set global variable once complete, refresh component.
      this.promise.then(() => {
        window.aceEditorLoaded = true;
      }).catch(error => {
        console.log(error); // eslint-disable-line no-console
      });
    } else {
      // Create a promise and resolve immediately if Ace is already loaded.
      this.promise = new Promise((resolve, reject) => { resolve(); });
    }
  }


  /*getInitialTree(storeState) {
    // For now, we are going to make sure that the debugger
    // doesn't let you edit anything beyond tile and entity sets.

    return {
      "tileSet": storeState.tileSet,
      "entitySet": storeState.entitySet
    };
  }*/

  getEditorContent() {
    return this.editor.getValue();
  }

  setEditorContent(content) {
    this.editor.setValue(content);
  }

  saveEditorContent() {
    let content = this.getEditorContent();
    let location = this.state.location;
    let [actor, event] = location.split(".");

    // Recompile
    compileScript(actor, content, event, true);
  }


  handleBrowserSelect(e) {
    let scriptName = e.target.dataset['scriptname'];

    this.setState({
      "location": scriptName
    });

    let [actor, event] = scriptName.split(".");
    let content = window.scriptEngineFunctions[actor][event]['payload'];

    this.setEditorContent(content);
  }


  handleRefresh(e) {
    e.preventDefault();
    this.setState({
      "storeState": this.store.getState()
    });
  }


  /*_generateBrowserItems(o) {
    if (isTrueObject(o)) {

      // Generate buttons
      let items = Object.keys(o).map((item) => {
        return (
          <button onClick={ this.handleBrowserSelect.bind(this) } data-keyName={ item } key={ item }>{ item }</button>
        );
      });

      // Prepend a "Go Back" button
      items.unshift(
        <button className="browser-up" onClick={ this.handleBrowserUp.bind(this) }> .. </button>
      );

      // Append a "New File" button
      items.push(
        <button className="new-field" onClick={ this.handleBrowserUp.bind(this) }>+ New Field +</button>
      );

    }
  }*/


  generateBrowserItems() {
    if (window.scriptEngineFunctions === undefined) {
      return [];
    }

    let scriptNames = [];

    Object.keys(window.scriptEngineFunctions).map((actor) => {
      Object.keys(window.scriptEngineFunctions[actor]).map((script) => {
        scriptNames.push(`${actor}.${script}`);
      });
    });

    let items = scriptNames.map((name) => {
      return (
        <li key={ name }>
          <button onClick={ this.handleBrowserSelect.bind(this) } data-scriptName={ name }>{ name }</button>
        </li>
      );
    });

    return items;
  }


  render() {
    let browserItems = this.generateBrowserItems();

    return (
      <div className="section-editor">
        <div className="editor-select">
          <h4> Browse </h4>
          <button className="refresh" onClick={ this.handleRefresh.bind(this) }>Refresh</button>
          <button className="compile" onClick={ this.saveEditorContent.bind(this) }>Compile</button>
          <ul className="item-browser">
            { browserItems }
          </ul>
        </div>
        <div className="editor-edit">
          <div className="code-editor" style="width: 100%; height: 600px;" ref={ (node) => this.refs.editor = node }>
            var x = "Hello! Select an item to edit first.";
          </div>
        </div>
      </div>
    );
  }
}
