import Inferno from "inferno";
import InfernoDOM from "inferno-dom";

import DungeonClient from "./Components/DungeonClient";
import DungeonInfo from "./Components/DungeonInfo";
import DebugTools from "./Components/DebugTools";
import Dungeon from "./Models/Dungeon";
import MiniMap from "./Models/MiniMap";

export default function Main() {
  let model = new Dungeon();
  let miniMap = new MiniMap();

  model.fetch().then(() => {
    InfernoDOM.render(
      <DungeonClient model={ model } miniMap={ miniMap } />,
      document.getElementById("dungeon-client-mount")
    );

    InfernoDOM.render(
      <DungeonInfo miniMap={ miniMap } />,
      document.getElementById("dungeon-info-mount")
    );

    InfernoDOM.render(
      <DebugTools regenerate={ model._debug_regenerate(true) } reveal={ model._debug_reveal(true) } />,
      document.getElementById("dungeon-debug-mount")
    );
  });
}

Main();
