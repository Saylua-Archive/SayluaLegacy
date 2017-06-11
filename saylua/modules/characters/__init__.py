# =======================================================
#
#  Characters -- A module for all things NPC and such.
#  ---------------------------------
#  NPCs.
#
# =======================================================

from saylua.routing import SayluaRouter
from . import urls

MODULE_NAME = 'characters'
IMPORT_NAME = __name__

blueprint = SayluaRouter.create_blueprint(MODULE_NAME, IMPORT_NAME)
blueprint.register_urls(urls.urlpatterns)
