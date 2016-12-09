# =======================================================
#
#  Trade -- Commerce module
#  ---------------------------------
#  Bank, shop NPCs, currency trading.
#
# =======================================================

from saylua.routing import SayluaRouter
from . import urls

MODULE_NAME = 'trade'
IMPORT_NAME = __name__

blueprint = SayluaRouter.create_blueprint(MODULE_NAME, IMPORT_NAME)
blueprint.register_urls(urls.urlpatterns)
