#=======================================================
#
#  Explore -- Dungeons, Exploration
#  ---------------------------------
#  Contains all Dungeons and Exploration related code.
#
#=======================================================

from saylua.routing import SayluaRouter
from . import urls

import os

module_name = os.path.basename(os.getcwd())
import_name = __name__

blueprint = SayluaRouter(
  module_name,
  import_name,
  static_folder='static',
  template_folder='templates',
  url_prefix=None
)

blueprint.register_urls(urls.urlpatterns)
