<?php
require_once 'vendor/autoload.php';
// Build a new entity
$obj_book = new GDS\Entity();
$obj_book->title = 'Romeo and Juliet';
$obj_book->author = 'William Shakespeare';
$obj_book->isbn = '1840224339';

// Write it to Datastore
$obj_store = new GDS\Store('Book');
$obj_store->upsert($obj_book);

$obj_store = new GDS\Store('Book');
foreach($obj_store->fetchAll() as $obj_book) {
    echo "Title: {$obj_book->title}, ISBN: {$obj_book->isbn} <br />", PHP_EOL;
}
