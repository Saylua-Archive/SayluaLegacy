from saylua.routing import url
from . import views


urlpatterns = [
    # Town Square.
    url('/town/', view_func=views.town_main, name='town', methods=['GET']),
    url('/free_items/', view_func=views.free_items, name='free_items', methods=['POST'])
]
