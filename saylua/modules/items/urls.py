from saylua.routing import url
from . import views

urlpatterns = [
    # Admin URLs
    url('/admin/items/add/', view_func=views.admin.admin_panel_items_add,
        name='items_admin_add', methods=['GET', 'POST']),
    url('/admin/items/edit/', view_func=views.admin.admin_panel_items_edit,
        name='items_admin_edit'),

    # Primary URLs
    url('/inventory/<category>/', view_func=views.items.items_inventory, name='items_inventory'),
    url('/inventory/', view_func=views.items.items_inventory, name='items_inventory'),
    url('/items/', view_func=views.items.items_view_all, name='items_view_all'),
    url('/items/<url_name>', view_func=views.items.items_view_single, name='items_view_single')
]
