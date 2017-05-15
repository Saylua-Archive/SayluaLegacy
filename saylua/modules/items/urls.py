from saylua.routing import url
from . import views

urlpatterns = [
    # Admin URLs
    url('/admin/items/add/', view_func=views.admin.admin_panel_items_add,
        name='admin_add', methods=['GET', 'POST']),
    url('/admin/items/edit/', view_func=views.admin.admin_panel_items_edit,
        name='admin_edit'),

    # Primary URLs
    url('/inventory/<category>/', view_func=views.items.items_inventory, name='inventory'),
    url('/inventory/', view_func=views.items.items_inventory, name='inventory'),
    url('/items/', view_func=views.items.items_view_all, name='view_all'),
    url('/items/<url_name>', view_func=views.items.items_view_single, name='view_single')
]
