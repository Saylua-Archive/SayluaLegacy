from saylua.routing import url
from . import views


urlpatterns = [
    url('/arcade/', view_func=views.games_main, name="games"),
    url('/arcade/blocks/', view_func=views.games_blocks),
    url('/arcade/space/', view_func=views.games_space)
]
