from saylua.routing import url
from . import views

urlpatterns = [
    url('/', view_func=views.home, name='home_main', methods=['GET']),
    url('/news/', view_func=views.news, name='home_news', methods=['GET']),
    url('/news/puzzle/', view_func=views.puzzle, name='home_puzzle', methods=['GET'])
]
