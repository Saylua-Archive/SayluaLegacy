from saylua.routing import url
from . import views

urlpatterns = [
  # Login URLs
  url('/login/', view_func=views.login.login, name='login', methods=['GET', 'POST']),
  url('/login/recover/', view_func=views.login.recover_login, name='login_recover'),
  url('/login/reset/<user>/<code>/', view_func=views.login.reset_password, name='login_reset'),
  url('/logout/', view_func=views.login.logout, name='logout'),
  url('/register/', view_func=views.login.register, name='register', methods=['GET', 'POST']),

  # Online users
  url('/online/', view_func=views.online.users_online, name='users_online'),

  # User Profile URls
  url('/user/', view_func=views.profile.user_profile_default, name='user_profile_default'),
  url('/user/<username>/', view_func=views.profile.user_profile, name='user_profile'),

  # User Settings URls
  url('/settings/', view_func=views.settings.user_settings, name='user_settings', methods=['GET', 'POST']),
  url('/settings/details/', view_func=views.settings.user_settings_details, name='user_settings_details', methods=['GET', 'POST']),
  url('/settings/css/', view_func=views.settings.user_settings_details, name='user_settings_details', methods=['GET', 'POST']),
  url('/settings/username/', view_func=views.settings.user_settings_username, name='user_settings_username', methods=['GET', 'POST']),
  url('/settings/username/release/', view_func=views.settings.user_settings_username_release, name='user_settings_username_release', methods=['POST']),
  url('/settings/email/', view_func=views.settings.user_settings_email, name='user_settings_email', methods=['GET', 'POST']),
  url('/settings/password/', view_func=views.settings.user_settings_password, name='user_settings_password', methods=['GET', 'POST'])
]
