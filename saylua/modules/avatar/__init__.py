# =======================================================
#
#  Avatar - Human Avatars
#  ---------------------------------
#  Contains code related to the human avatar dressup feature.
#
# =======================================================

from saylua.routing import SayluaRouter
from . import urls

MODULE_NAME = 'avatar'
IMPORT_NAME = __name__

blueprint = SayluaRouter.create_blueprint(MODULE_NAME, IMPORT_NAME)
blueprint.register_urls(urls.urlpatterns)
