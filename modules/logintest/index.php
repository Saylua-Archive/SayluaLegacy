<?php
use google\appengine\api\users\UserService;

$user = UserService::getCurrentUser();

if (isset($user)) {
    echo sprintf('Welcome, %s! (<a href="%s">sign out</a>)',
        $user->getNickname(),
        UserService::createLogoutUrl('/'));
} else {
    echo sprintf('<a href="%s">Sign in or register</a>',
        UserService::createLoginUrl('/'));
}
