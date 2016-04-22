<?php include('top.php'); ?>

<h2>Dress up your Human Avatar</h2>

<div style="width:250px; float:left;position: relative; top: 0; left: 0;" id="ha">
  <img src="static/img/ha.png" style="position: relative; top: 0; left: 0;">
</div>
<div>
<?php
$dir = 'static/img/ha/';
$files = scandir($dir);
foreach ($files as $f) {
  if ($f != "." && $f != "..") {
    echo '<a href="javascript:addItem(\'' . $dir. $f . '\');">' . $f . '</a> ';
  }
}
?>
</div>

<script>
var ha = document.getElementById("ha");
function addItem(item) {
  var placed = document.getElementById(item);
  if (placed) {
    placed.remove();
    return;
  }
  var img = document.createElement("img");
  img.setAttribute('src', item);
  img.id = item;
  img.style.position = "absolute";
  img.style.zIndex = "999";
  img.style.left = "0";
  img.style.top = "0";
  ha.appendChild(img);
}

Element.prototype.remove = function() {
    this.parentElement.removeChild(this);
}
NodeList.prototype.remove = HTMLCollection.prototype.remove = function() {
    for(var i = this.length - 1; i >= 0; i--) {
        if(this[i] && this[i].parentElement) {
            this[i].parentElement.removeChild(this[i]);
        }
    }
}
</script>
<?php include('bottom.php'); ?>
