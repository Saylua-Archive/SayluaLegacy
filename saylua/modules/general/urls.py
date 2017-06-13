from saylua.routing import url
from . import views

urlpatterns = [
    url('/', view_func=views.main.home, name='main', methods=['GET']),
    url('/landing/', view_func=views.main.landing, name='landing', methods=['GET']),
    url('/banned/', view_func=views.main.banned, name='banned', methods=['GET']),

    url('/news/', view_func=views.news.newspaper, name='news', methods=['GET']),
    url('/news/puzzle/', view_func=views.news.puzzle, name='puzzle', methods=['GET']),

    url('/page/<template>/', view_func=views.main.view_page, name='view_page')
]
