# =======================================================
#
#  House -- Your home in Saylua.
#  ---------------------------------
#  Contains the main view of your house where you live and your pets play.
#
# =======================================================

from saylua.routing import SayluaRouter
from . import urls

MODULE_NAME = 'house'
IMPORT_NAME = __name__

blueprint = SayluaRouter.create_blueprint(MODULE_NAME, IMPORT_NAME)
blueprint.register_urls(urls.urlpatterns)
