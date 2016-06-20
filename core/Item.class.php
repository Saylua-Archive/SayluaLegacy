<?php
class Item {
  private $data;

  function __construct(array $item_data) {
    $this->data = $item_data;
  }

  function setData($key, $value) {
    $this->data[$key] = $value;
  }

  function getData($key) {
    return $this->data[$key];
  }

  function getName() {
    return $this->name;
  }

  function isClothing() {
    return $this->type == "clothing";
  }

}
