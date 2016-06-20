<?php

class User {
  private static $item_database;

  function __construct() {
    // Constructor here
    if (!$this::$item_database) {
      $dir = 'static/img/ha/';
      $files = scandir($dir);
      foreach ($files as $f) {
        if ($f != "." && $f != "..") {
          
        }
      }
    }
  }

  function getInventoryItems($offset = 0, $limit = 30) {
    return $this::$item_database;
  }

  function getHA() {
    return "/static/img/ha.png";
  }

  function getBio() {
    return "Hi I'm User! ";
  }

  function getDisplayName() {
    return "User the User";
  }

  function getLink() {
    return "<a href='/user/user'>User the User</a>";
  }
}
