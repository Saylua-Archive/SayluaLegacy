# =======================================================
#
#  Search -- Both hands behind your head, sir.
#  ---------------------------------
#  TSA related code.
#
# =======================================================

from saylua.routing import SayluaRouter
from . import urls

MODULE_NAME = 'search'
IMPORT_NAME = __name__

blueprint = SayluaRouter.create_blueprint(MODULE_NAME, IMPORT_NAME)
blueprint.register_urls(urls.urlpatterns)
