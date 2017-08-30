// TODO: Submit a PR for htmlFor in eslint-inferno. This rule is no longer valid.
/* eslint { inferno/no-unknown-property: 0 } */
import Inferno from "inferno";

// We are creating the actions and options this way primarily
// so that we can add a search function in the future.

function mapActionsToButtons(props, state) {
  let actions = [
    ["Regenerate Dungeon", props.debugRegenerateDungeon],
    ["Reveal Map", props.debugRevealMap],
    ["Clear Cache", props.debugClearCache]
  ];

  let items = actions.map((action) => (
    <li key={ action[0].toLowerCase().replace(/\s/gi, "-") }>
      <button onClick={ action[1] }>{ action[0] }</button>
    </li>
  ));

  return items;
}

function mapOptionsToInputs(props, state) {
  let actions = [
    {
      "name": "FOV Enabled",
      "type": "toggle",
      "options": {
        "boundFunction": props.debugToggleOption.bind(this, 'FOVEnabled')
      },
      "value": state.debug.FOVEnabled
    },
    {
      "name": "Show Collision Map",
      "type": "toggle",
      "options": {
        "boundFunction": props.debugToggleOption.bind(this, 'showCollisions')
      },
      "value": state.debug.showCollisions
    },
    {
      "name": "Capture Keyboard Input",
      "type": "toggle",
      "options": {
        "boundFunction": props.debugToggleOption.bind(this, 'keyboardInputEnabled')
      },
      "value": state.debug.keyboardInputEnabled
    },
    {
      "name": "Enable Update Timers",
      "type": "toggle",
      "options": {
        "boundFunction": props.debugToggleOption.bind(this, 'enableUpdateTimers')
      },
      "value": state.debug.enableUpdateTimers
    }
  ];

  let items = actions.map((action) => {
    if (action.type === "toggle") {
      let sanitizedName = action.name.toLowerCase().replace(/\s/gi, "_");
      let elementID = `toggle-${sanitizedName}`;

      return (
        <li key={ `key-li-${ elementID }` }>
          <input
            id={ elementID }
            class={ `state-${ action.value }` }
            type="checkbox"
            checked={ action.value }
          />
          <label onClick={ action.options.boundFunction } for={ elementID }>
            { action.name }
            <div className="fake-checkbox"></div>
          </label>
        </li>
      );
    }
  });

  return items;
}

export default function DebugGeneral(props) {
  let state = props.store.getState();

  return (
    <div className="section-general">
      <div className="general-actions">
        <h4>Actions</h4>
        <ul>
          { mapActionsToButtons(props, state) }
        </ul>
      </div>
      <div className="general-options">
        <h4>Options</h4>
        <ul>
          { mapOptionsToInputs(props, state) }
        </ul>
      </div>
    </div>
  );
}
