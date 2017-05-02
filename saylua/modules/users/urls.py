from saylua.routing import url
from . import views

urlpatterns = [
    # Login URLs
    url('/login/', view_func=views.login.login, name='login', methods=['GET', 'POST']),
    url('/login/recover/', view_func=views.login.recover_login, name='login_recover',
        methods=['GET', 'POST']),
    url('/login/reset/<user>/<code>/', view_func=views.login.reset_password, name='login_reset'),
    url('/logout/', view_func=views.login.logout, name='logout'),
    url('/register/', view_func=views.login.register, name='register', methods=['GET', 'POST']),

    # Online users
    url('/online/', view_func=views.online.users_online, name='online'),

    # User Profile URls
    url('/user/', view_func=views.profile.user_profile_default, name='profile_default'),
    url('/user/<username>/', view_func=views.profile.user_profile, name='profile'),

    # User Settings URls
    url('/settings/', view_func=views.settings.user_settings, name='settings',
        methods=['GET', 'POST']),
    url('/settings/details/', view_func=views.settings.user_settings_details,
        name='settings_details', methods=['GET', 'POST']),
    url('/settings/username/', view_func=views.settings.user_settings_username,
        name='settings_username', methods=['GET', 'POST']),
    url('/settings/username/release/', view_func=views.settings.user_settings_username_release,
        name='settings_username_release', methods=['POST']),
    url('/settings/email/', view_func=views.settings.user_settings_email,
        name='settings_email', methods=['GET', 'POST']),
    url('/settings/password/', view_func=views.settings.user_settings_password,
        name='settings_password', methods=['GET', 'POST']),

    # Admin views
    url('/admin/user/', view_func=views.admin.user_manage,
        name='user_manage', methods=['GET', 'POST']),
    url('/admin/user/invite/', view_func=views.admin.user_invite,
        name='user_invite', methods=['GET', 'POST']),
]
