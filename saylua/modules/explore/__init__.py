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
IMPORT_NAME = __name__

blueprint = SayluaRouter.create_blueprint(MODULE_NAME, IMPORT_NAME)
blueprint.register_urls(urls.urlpatterns)
