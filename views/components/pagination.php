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
$this->totalPages = 10;

$pageBuffer = 2;

$startPageRange = $this->currentPage - $pageBuffer;
$endPageRange = $this->currentPage + $pageBuffer;
if ($this->currentPage <= $pageBuffer) {
  $endPageRange += $pageBuffer - $this->currentPage;
  $startPageRange = 1;
}

if ($endPageRange > $this->totalPages) {
  $endPageRange = $this->totalPages;
}
?>
<div class="pagination">
  <a href="#">&#8592; Prev</a>
  <a href="#">1</a>
  <a href="#">2</a>
  <a href="#">3</a>
  <a href="#">4</a>
  <span class="active">5</span>
  <span>...</span>
  <a href="#">1000</a>
  <a href="#">Next &#8594;</a>
</div>
