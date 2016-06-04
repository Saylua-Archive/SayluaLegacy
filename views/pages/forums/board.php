<?php include('./views/layout/top.php'); ?>
<h2>Viewing Sample Board</h2>
<span class="breadcrumb">
  <a href="/forums">Forums</a> &#187; Sample Board
</span>
<div class="center">
<?php include('./views/components/pagination.php'); ?>
</div>

<table class="forum-table">
  <tr>
    <th class="section-header" colspan="5">
      Threads in Sample Board
      <a class="right normal" href="#write-forum-thread">
        <img src="/static/img/icons/pencil.png">
        Make a New Thread
      </a>
    </th>
  </tr>
  <tr>
    <th>
    </th>
    <th>
      Thread Title
    </th>
    <th>
      Replies
    </th>
    <th>
      Started By
    </th>
    <th>
      Last Post
    </th>
  </tr>

  <? for ($i = 0; $i < 5; $i++): ?>
    <tr class="forum-thread-row">
      <td class="forum-thread-icon">
        <? if ($i == 3): ?>
        <img src="/static/img/icons/lock.png">
        <? endif ?>
      </td>
      <td class="forum-thread-info">
        <a href="/forums/thread">
          <span class="forum-thread-link">Sample Thread</span>
          <p class="small">Created on May 5, 2016 at 6:21 PM</p>
        </a>
      </td>
      <td>
        5
      </td>
      <td>
        <a href="/user">User</a>
      </td>
      <td class="forum-latest-post">
        by <a href="/user">User</a>
        on 5 May 2016 21:05 SST
      </td>
    </tr>
  <? endfor; ?>
</table>

<div class="center">
<?php include('./views/components/pagination.php'); ?>
</div>

<table class="forum-table form-table" id="write-forum-thread">
  <tr>
    <th class="section-header" colspan="2">
      Quick Thread
    </th>
  </tr>
  <tr>
    <td class="label"><label for="forum-thread-title">Thread Title</label></td>
    <td>
      <input type="text" placeholder="Thread Title" id="forum-thread-title">
    </td>
  </tr>
  <tr>
    <td class="label"><label for="forum-thread-body">Thread Body</label></td>
    <td>
      <textarea placeholder="Thread Content" id="forum-thread-body"></textarea>
    </td>
  </tr>
  <tr>
    <td colspan="2" class="center">
      <input type="submit" value="Post New Thread" name="post">
      <input type="submit" value="Preview Thread" name="preview">
    </td>
  </tr>
</table>
<?php include('./views/layout/bottom.php'); ?>
