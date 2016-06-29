<?php include('./views/layout/top.php'); ?>
<h2>Login to Saylua</h2>

<input type="text" placeholder="Username" name="username">
<input type="password" placeholder="Password" name="password">
<input type="submit" value="Login" name="login">
<p><a href="/login/recover">Lost username or password?</a></p>
<p><a href="/register">Register a new account! </a></p>
<?php include('./views/layout/bottom.php'); ?>
