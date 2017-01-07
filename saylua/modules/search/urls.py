from saylua.routing import url
from . import views


urlpatterns = [
    url('/search/', view_func=views.site_search, name="search")
]
