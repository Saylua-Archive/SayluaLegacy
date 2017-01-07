from saylua.routing import url
from . import views


urlpatterns = [
    # Town Square.
    url('/town/', view_func=views.town_main, name='town')
]
