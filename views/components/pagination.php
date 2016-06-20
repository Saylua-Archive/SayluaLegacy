<?php
/*
 * Variables
 * $this->pageUrlBase
 * $this->pageUrlEnd
 * $this->currentPage
 * $this->totalPages
 */
if (!isset($this->pageUrlEnd)) {
  $this->pageUrlEnd = "";
}

if (!isset($this->pageUrlBase)) {
  $this->pageUrlBase = "?page=";
}

$this->currentPage = 5;
if (isset($_GET['page'])) {
  $this->currentPage = intval($_GET['page']);
}
$this->totalPages = 10;

$pageBuffer = 2;

$startPageRange = $this->currentPage - $pageBuffer;
$endPageRange = $this->currentPage + $pageBuffer;
if ($startPageRange < 1) {
  $endPageRange += -$startPageRange + 1;
  $startPageRange = 1;
}

if ($endPageRange > $this->totalPages) {
  $startPageRange -= $endPageRange - $this->totalPages;
  $startPageRange = max($startPageRange, 1);
  $endPageRange = $this->totalPages;
}
?>
<div class="pagination">
<? if ($this->currentPage > 1): ?>
  <a href="<?=$this->pageUrlBase .
    ($this->currentPage - 1) . $this->pageUrlEnd ?>">&#8592; Prev</a>
<? else: ?>
  <span>&#8592; Prev</span>
<? endif ?>

<? if ($startPageRange > 1): ?>
  <a href="<?=$this->pageUrlBase . "1" . $this->pageUrlEnd ?>">1</a>
  <span>...</span>
<? endif ?>

<? for ($i = $startPageRange; $i <= $endPageRange; $i++ ): ?>
<? if ($i == $this->currentPage): ?>
  <span class="active"><?=$i ?></span>
<? else: ?>
  <a href="<?=$this->pageUrlBase . $i
    . $this->pageUrlEnd ?>"><?=$i ?></a>
<? endif ?>
<? endfor ?>

<? if ($endPageRange < $this->totalPages): ?>
  <span>...</span>
  <a href="<?=$this->pageUrlBase . $this->totalPages
    . $this->pageUrlEnd ?>"><?=$this->totalPages ?></a>
<? endif ?>

<? if ($this->currentPage < $this->totalPages): ?>

  <a href="<?=$this->pageUrlBase . ($this->currentPage + 1)
  . $this->pageUrlEnd ?>">Next &#8594;</a>
<? else: ?>
  <span>Next &#8594;</span>
<? endif ?>
</div>
