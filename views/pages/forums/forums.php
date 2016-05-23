<?php include('./views/layout/top.php'); ?>
<h2>Forums</h2>
<table class="forum-boards">
  <tr>
    <th colspan="5" class="category-header">Category Name</th>
  </tr>
  <tr>
    <td></td>
    <th>
      Forum
    </th>
    <th>
      Threads
    </th>
    <th>
      Posts
    </th>
    <th>
      Latest Post
    </th>
  </tr>
<? for ($i = 0; $i < 10; $i++): ?>
  <tr class="forum-board-row">
    <td class="forum-board-icon">
      <img src="/static/img/SHC.png">
    </td>
    <td class="forum-board-info">
      <a href="/forums/board">Sample Board</a>
      <p>
        Sample board is the best place to table about anything.
      </p>
    </td>
    <td>
      5
    </td>
    <td>
      322
    </td>
    <td class="forum-latest-post">
      <a href="/forums/thread">Sample Thread is the world's longest
        thread title</a> by <a href="/user">User</a>
      on 5 May 2016 21:05 SST
    </td>
  </tr>
<? endfor; ?>
</table>
<?php include('./views/layout/bottom.php'); ?>
