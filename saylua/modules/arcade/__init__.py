# =======================================================
#
#  Games -- Game Nonsense
#  ---------------------------------
#  Come one, come all, it's Saturday At The Arcade!
#
# =======================================================

from saylua.routing import SayluaRouter
from . import urls

MODULE_NAME = 'arcade'
IMPORT_NAME = __name__

blueprint = SayluaRouter.create_blueprint(MODULE_NAME, IMPORT_NAME)
blueprint.register_urls(urls.urlpatterns)
