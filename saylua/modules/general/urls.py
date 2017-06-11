from saylua.routing import url
from . import views

urlpatterns = [
    url('/', view_func=views.home, name='main', methods=['GET']),
    url('/landing/', view_func=views.landing, name='landing', methods=['GET']),
    url('/banned/', view_func=views.banned, name='banned', methods=['GET']),
    url('/news/', view_func=views.news, name='news', methods=['GET']),
    url('/news/puzzle/', view_func=views.puzzle, name='puzzle', methods=['GET'])
]
