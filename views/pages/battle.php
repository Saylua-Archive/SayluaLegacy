<?php
$this->fullscreen = true;
include('./views/layout/top.php');
?>
<h2>You are in a battle! </h2>
<div id="battle-screen">
  <div class="side left">
    <div class="battler player left bounce">
      <img src="/static/img/SHC.png" class="left flipped">
      <div class="stat-meter health">
        <div style="width:80%;"></div>
        <span>24/32 Health</span>
      </div>
      <div class="stat-meter stamina">
        <div style="width:100%;"></div>
        <span>24/32 Stamina</span>
      </div>
    </div>
    <div class="battler player left bounce">
      <img src="/static/img/SHC.png" class="left flipped">
      <div class="stat-meter health">
        <div style="width:8%;"></div>
        <span>24/32 Health</span>
      </div>
      <div class="stat-meter stamina">
        <div style="width:100%;"></div>
        <span>24/32 Stamina</span>
      </div>
    </div>
    <div class="battler player left bounce">
      <img src="/static/img/SHC.png" class="left flipped">
      <div class="stat-meter health">
        <div style="width:100%;"></div>
        <span>24/32 Health</span>
      </div>
      <div class="stat-meter stamina">
        <div style="width:100%;"></div>
        <span>24/32 Stamina</span>
      </div>
    </div>
  </div>

  <div class="side right">
    <div class="battler enemy right bounce">
      <img src="/static/img/velbird.png" class="flipped right">

      <div class="stat-meter health">
        <div style="width:100%;"></div>
        <span>24/32 Health</span>
      </div>
      <div class="stat-meter stamina">
        <div style="width:100%;"></div>
        <span>24/32 Stamina</span>
      </div>
    </div>
    <div class="battler enemy right bounce">
      <img src="/static/img/velbird.png" class="flipped right">

      <div class="stat-meter health">
        <div style="width:100%;"></div>
        <span>24/32 Health</span>
      </div>
      <div class="stat-meter stamina">
        <div style="width:100%;"></div>
        <span>24/32 Stamina</span>
      </div>
    </div>
    <div class="battler enemy right bounce">
      <img src="/static/img/velbird.png" class="flipped right">

      <div class="stat-meter health">
        <div style="width:100%;"></div>
        <span>24/32 Health</span>
      </div>
      <div class="stat-meter stamina">
        <div style="width:100%;"></div>
        <span>24/32 Stamina</span>
      </div>
    </div>
  </div>
</div>
<?php include('./views/layout/bottom.php'); ?>
