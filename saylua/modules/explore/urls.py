from saylua.routing import url
from . import views

urlpatterns = [
  url('/explore/', view_func=views.home, name='explore_home', methods=['GET']),
  url('/battle/', view_func=views.battle, name='explore_battle', methods=['GET'])
]
