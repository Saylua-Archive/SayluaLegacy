from saylua.routing import url
from . import views

urlpatterns = [
    url('/', view_func=views.main.home, name='home', methods=['GET']),
    url('/landing/', view_func=views.main.landing, name='landing', methods=['GET']),
    url('/banned/', view_func=views.main.banned, name='banned', methods=['GET']),

    url('/news/', view_func=views.news.newspaper, name='news', methods=['GET']),
    url('/news/puzzle/', view_func=views.news.puzzle, name='puzzle', methods=['GET']),

    url('/page/<template>/', view_func=views.main.view_page, name='view_page'),

    url('/theme/change/', view_func=views.main.change_theme, name='change_theme', methods=['POST']),

    url('/intro/side/', view_func=views.main.intro_side, name='intro_side', methods=['GET', 'POST']),
    url('/intro/companion/', view_func=views.main.intro_companion, name='intro_companion', methods=['GET', 'POST']),
    url('/intro/avatar/', view_func=views.main.intro_avatar, name='intro_avatar', methods=['GET', 'POST'])
]
