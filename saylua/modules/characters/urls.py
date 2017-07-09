from saylua.routing import url

from . import views


urlpatterns = [
    url('/characters/', view_func=views.character_list, name='list'),
    url('/character/<canon_name>', view_func=views.character_profile, name='profile'),
]
