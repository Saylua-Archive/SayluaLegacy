<?php include('./views/layout/top.php'); ?>
<h2>Viewing Sample Thread</h2>
<span class="breadcrumb">
  <a href="/forums">Forums</a> &#187;
  <a href="/forums/board/1">Sample Board</a> &#187;
  Sample Thread
</span>

<div class="full normal">
  <div class="left">
    <a class="tiny-button" href="#write-forum-reply">
      <img src="/static/img/icons/pencil.png">
      Write a Reply
    </a>
    <a class="tiny-button" href="#">
      <img src="/static/img/icons/transmit.png">
      Bump Topic
    </a>
  </div>

  <div class="right">
    <a class="tiny-button" href="#">
      <img src="/static/img/icons/bell.png">
      Subscribe
    </a>
  </div>
</div>

<div class="center">
<?php include('./views/components/pagination.php'); ?>
</div>
<? for ($i = 0; $i < 10; $i++): ?>
<table class="forum-post" id="forum-post-<?=$i ?>">
  <tr>
    <th colspan="2">
      <a href="#forum-post-<?=$i ?>">Post in Really Long Sample...</a> |
      4 June 2016 5:21 SST
      <span class="right">
        <a href="#">Quote</a>  |
        <a href="#">Modify</a>
      </span>
    </th>
  </tr>
  <tr>
    <td class="forum-post-info">
      <a href="/ha"><img src="/static/img/ha.png"></a>
    </td>
    <td class="forum-post-body">
      <p>
        User loves making forum posts, hello everyone. I need to type
        a onger thread because of my new job as a tester.
      </p>
      <div class="divider"></div>
      User has a signature too.
    </td>
  </tr>
</table>
<? endfor ?>

<div class="center">
<?php include('./views/components/pagination.php'); ?>
</div>

<table class="forum-table form-table" id="write-forum-reply">
  <tr>
    <th class="section-header">
      Write a New Reply
    </th>
  </tr>
  <tr>
    <td class="center">
      <textarea placeholder="Type your post content here" id="forum-post-body"></textarea>
    </td>
  </tr>
  <tr>
    <td class="center">
      <input type="submit" value="Post New Reply" name="post">
      <input type="submit" value="Preview Reply" name="preview">
    </td>
  </tr>
</table>
<?php include('./views/layout/bottom.php'); ?>
