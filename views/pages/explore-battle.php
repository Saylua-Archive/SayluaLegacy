<?php
$fullscreen = true;
include('./views/layout/top.php');
?>
<h2>You are in a battle! </h2>
<div id="battle-screen">
  <div class="side left">
    <img src="/static/img/SHC.png" class="battler left bounce flipped">
    <img src="/static/img/SHC.png" class="battler left bounce flipped">
    <img src="/static/img/SHC.png" class="battler left bounce flipped">
  </div>

  <div class="side right">
    <img src="/static/img/velbird.png" class="flipped battler right bounce enemy">
    <img src="/static/img/velbird.png" class="flipped battler right bounce enemy">
    <img src="/static/img/velbird.png" class="flipped battler right bounce enemy">
  </div>
</div>
<?php include('./views/layout/bottom.php'); ?>
