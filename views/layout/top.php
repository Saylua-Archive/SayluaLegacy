<!doctype html>

<html lang="en">
<head>
  <meta charset="utf-8">

  <title>Saylua</title>
  <meta name="description" content="A new virtual petsite. ">
  <meta name="author" content="Saylua">

  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.6.1/css/font-awesome.min.css">
  <link rel="stylesheet" href="/static/css/styles.min.css">
  <script src="/static/js/main.min.js"></script>

<?php if (isset($header_scripts)): ?>
<?php foreach ($header_scripts as $script): ?>
  <script src="/static/js/<?=$script?>"></script>
<?php endforeach ?>
<?php endif ?>

  <link href='https://fonts.googleapis.com/css?family=Satisfy' rel='stylesheet' type='text/css'>
  <link href='https://fonts.googleapis.com/css?family=Kaushan+Script' rel='stylesheet' type='text/css'>
  <!--[if lt IE 9]>
  <script src="http://html5shiv.googlecode.com/svn/trunk/html5.js"></script>
  <![endif]-->
</head>

<body>
<div id="logo" class="container">
    <a href="/">Saylua</a>
</div>
<div id="navbar" class="container">
  <div class="content-width">
    <a href="/">Home</a>
    <a href="/explore">Explore</a>
    <a href="/forums">Community</a>
    <a href="/games">Games</a>
    <a href="/shops">Shops</a>
    <a href="/quests">Quests</a>

    <form class="search" action="/search">
      <input type="text" placeholder="Seach Saylua" name="q">
      <button><i class="fa fa-search" aria-hidden="true"></i></button>

    </form>
  </div>
</div>
<div class="container">
  <div class="content">
<?php
if (!$fullscreen) {
  include('sidebars.php');
}
?>
    <div class="page-area">
<?php
if ($_SESSION['random_event']) {
  include('random-event.php');
  unset($_SESSION['random_event']);
}
?>
