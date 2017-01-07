from saylua.routing import url
from . import views

urlpatterns = [
    url('/admin/', view_func=views.admin_panel, name='admin_home'),
    url('/admin/roles/add/', view_func=views.admin_panel_roles_add, name='admin_role_add', methods=['GET', 'POST']),
    url('/admin/roles/edit/', view_func=views.admin_panel_roles_edit, name='admin_role_edit', methods=['GET', 'POST']),
    url('/admin/setupdb/', view_func=views.setup_db, name='admin_setup_db')
]
