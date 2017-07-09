from saylua.routing import url
from . import views

urlpatterns = [
    url('/house/', view_func=views.main.house, name='house', methods=['GET']),
]
