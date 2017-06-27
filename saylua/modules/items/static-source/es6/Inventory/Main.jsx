import Inferno from "inferno";

import Inventory from "./Inventory";
import InventoryModel from "./InventoryModel";

let model = new InventoryModel();

Inferno.render(
  <Inventory model={ model } />,
  document.getElementById("inventory-mount")
);
