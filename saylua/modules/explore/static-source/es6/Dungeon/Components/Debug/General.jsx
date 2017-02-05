import Inferno from "inferno";

// We are creating the actions and options this way primarily
// so that we can add a search function in the future.

function mapActionsToButtons(props) {
  let actions = [
    ["Regenerate Dungeon", props.debugRegenerateDungeon],
    ["Reveal Tiles", props.debugRevealMap]
  ];

  let items = actions.map((action) => (
    <li>
      <button onClick={ action[1] }>{ action[0] }</button>
    </li>
  ));

  return items;
}

function mapOptionsToInputs(props) {
  let actions = [
    {
      "name": "Enable FOV",
      "type": "toggle",
      "options": {
        "boundFunction": props.debugEnableFOV
      }
    }
  ];

  let items = actions.map((action) => (
    <li>
      <button onClick={ action[1] }>{ action[0] }</button>
    </li>
  ));

  return items;
}

export default function DebugGeneral(props) {
  return (
    <div className="section-general">
      <div className="general-actions">
        <h4>Actions</h4>
        <ul>
          { mapActionsToButtons(props) }
        </ul>
      </div>
      <div className="general-options">
        <h4>Options</h4>
        <ul>
        </ul>
      </div>
    </div>
  );
}
