<?php
function render_template($name) {
  $view_path = "./views/";
  include($view_path . $name);
}
