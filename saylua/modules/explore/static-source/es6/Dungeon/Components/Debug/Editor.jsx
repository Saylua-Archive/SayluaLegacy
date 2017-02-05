/* global ace */
// Editor -> Required by DebugTools
// --------------------------------------
// Allows developers to edit entity / tile
// fields and scripts.

import Inferno from "inferno";
import Component from "inferno-component";

import { injectScript } from "Utils";

export default class DebugEditor extends Component {
  constructor(props) {
    super(props);

    this.state = {
      "selected": {
        "location": undefined,
        "content": undefined
      },
      "browserObj": {},
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

  handleRefresh(e) {
    e.preventDefault();
    this.setState({
      "_forceUpdate": !this.state._forceUpdate
    });
  }

  render() {
    return (
      <div className="section-editor">
        <div className="editor-select">
          <h4> Browse </h4>
          <button onClick={ this.handleRefresh.bind(this) }>Refresh</button>
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
