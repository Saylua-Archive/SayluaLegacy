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
    url('/item/<canon_name>/', view_func=views.items.items_view_single, name='view_single'),

    # Item APIS
    url('/api/inventory/<int:category_id>/<int:page>/',
        view_func=views.api.api_inventory, name='api_inventory'),

    url('/autosale/', view_func=views.actions.autosale,
        name='autosale', methods=['POST']),
    url('/mini/bond/', view_func=views.actions.bond_mini,
        name='bond_mini', methods=['POST'])
]
