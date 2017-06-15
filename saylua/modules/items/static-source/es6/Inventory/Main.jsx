import Inferno from "inferno";

import ItemModal from "./ItemModal";

Inferno.render(
  <ItemModal itemName="fruit" itemImage="image" closed={ false } />,
  document.getElementById("inventory-modal")
);
