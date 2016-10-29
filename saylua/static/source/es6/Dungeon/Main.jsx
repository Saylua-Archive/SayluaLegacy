import Inferno from "inferno";
import InfernoDOM from "inferno-dom";

import DungeonClient from "./Components/DungeonClient";
import Dungeon from "./Models/Dungeon";

export default function Main() {
  let model = new Dungeon();

  model.fetch().then(() => {
    InfernoDOM.render(<DungeonClient model={ model } />, document.getElementById("dungeon-client-mount"));
  });
}

Main();
