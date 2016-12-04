#=======================================================
#
#  Explore -- Dungeons, Exploration
#  ---------------------------------
#  Contains all Dungeons and Exploration related code.
#
#=======================================================

from saylua.routing import SayluaRouter
from . import urls

MODULE_NAME = 'explore'

blueprint = SayluaRouter(
  MODULE_NAME,
  __name__,
  static_folder='static',
  template_folder='templates',
  static_url_path='/static/{}'.format(MODULE_NAME),
  url_prefix=None
)

blueprint.register_urls(urls.urlpatterns)
