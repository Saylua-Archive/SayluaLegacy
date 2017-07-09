# =======================================================
#
#  Commerce -- Commerce module
#  ---------------------------------
#  Bank, shops, currency trading.
#
# =======================================================

from saylua.routing import SayluaRouter
from . import urls

MODULE_NAME = 'commerce'
IMPORT_NAME = __name__

blueprint = SayluaRouter.create_blueprint(MODULE_NAME, IMPORT_NAME)
blueprint.register_urls(urls.urlpatterns)
