# =======================================================
#
#  Home -- The first page you see on Saylua, maybe.
#  ---------------------------------
#  Contains landing page related code.
#
# =======================================================

from saylua.routing import SayluaRouter
from . import urls

MODULE_NAME = 'hom'
IMPORT_NAME = __name__

blueprint = SayluaRouter.create_blueprint(MODULE_NAME, IMPORT_NAME)
blueprint.register_urls(urls.urlpatterns)
