from saylua.routing import url
from . import views

urlpatterns = [
  url('/explore/', view_func=views.explore_home, name='explore_home', methods=['GET'])
]
