from saylua.routing import url
from . import views

urlpatterns = [
    url('/admin/', view_func=views.admin_panel, name='admin_home')
]
