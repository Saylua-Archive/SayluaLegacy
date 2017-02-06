import Inferno from "inferno";

// We are creating the actions and options this way primarily
// so that we can add a search function in the future.

function mapActionsToButtons(props, state) {
  let actions = [
    ["Regenerate Dungeon", props.debugRegenerateDungeon],
    ["Reveal Map", props.debugRevealMap]
  ];

  let items = actions.map((action) => (
    <li>
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
        "boundFunction": props.debugEnableFOV
      },
      "value": state.debug.FOVEnabled
    }
  ];

  let items = actions.map((action) => {
    if (action.type === "toggle") {
      let sanitizedName = action.name.toLowerCase().replace(" ", "_");
      let elementID = `toggle-${sanitizedName}`;

      return (
        <li>
          <input
            id={ elementID }
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
