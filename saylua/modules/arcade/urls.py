from saylua.routing import url
from . import views


urlpatterns = [
  url('/arcade/', view_func=views.games_main),
  url('/games/', view_func=views.games_main, name="games")
]
