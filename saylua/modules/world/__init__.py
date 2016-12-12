# =======================================================
#
#  World -- Module for the overworld of Saylua.
#  ---------------------------------
#  Towns, cities, and other general location pages.
#
# =======================================================

from saylua.routing import SayluaRouter
from . import urls

MODULE_NAME = 'world'
IMPORT_NAME = __name__

blueprint = SayluaRouter.create_blueprint(MODULE_NAME, IMPORT_NAME)
blueprint.register_urls(urls.urlpatterns)
