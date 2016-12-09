# =======================================================
#
#  Users -- User Related Pages
#  ---------------------------------
#  User state management, settings, information.
#
# =======================================================

from saylua.routing import SayluaRouter
from . import urls

MODULE_NAME = 'users'
IMPORT_NAME = __name__

blueprint = SayluaRouter.create_blueprint(MODULE_NAME, IMPORT_NAME)
blueprint.register_urls(urls.urlpatterns)
