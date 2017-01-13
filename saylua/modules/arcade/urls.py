from saylua.routing import url
from . import views, api


urlpatterns = [
    url('/arcade/', view_func=views.games_main, name="games"),
    url('/arcade/blocks/', view_func=views.games_blocks),
    url('/arcade/space/', view_func=views.games_space),
    url('/api/arcade/score/<int:game>/', methods=['POST'], view_func=api.api_send_score)
]
