# =======================================================
#
#  Admin -- Saylua Admin
#  ---------------------------------
#  Administration related code, all templates for admin
#  are located at the root level, not here.
#
# =======================================================

from saylua.routing import SayluaRouter
from . import urls

MODULE_NAME = 'admin'
IMPORT_NAME = __name__

blueprint = SayluaRouter.create_blueprint(MODULE_NAME, IMPORT_NAME)
blueprint.register_urls(urls.urlpatterns)
