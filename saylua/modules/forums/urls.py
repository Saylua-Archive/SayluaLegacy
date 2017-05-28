from saylua.routing import url
from . import admin_views
from . import views


urlpatterns = [
    # Admin Views
    url('/admin/forums/boards/', view_func=admin_views.manage_boards,
        name='admin_boards', methods=['GET', 'POST']),
    url('/admin/forums/boards/<canon_name>/', view_func=admin_views.edit_board,
        name='admin_board_edit', methods=['GET', 'POST']),
    url('/admin/forums/categories/', view_func=admin_views.manage_categories,
        name='admin_categories', methods=['GET', 'POST']),
    url('/admin/forums/categories/<canon_name>/', view_func=admin_views.edit_category,
        name='admin_category_edit', methods=['GET', 'POST']),

    # Primary Views
    url('/forums/', view_func=views.forums_home, name='forum_home'),
    url('/forums/board/<canon_name>/', view_func=views.forums_board,
        name='forum_board', methods=['GET', 'POST']),
    url('/forums/thread/<thread_id>/', view_func=views.forums_thread,
        name='forum_thread', methods=['GET', 'POST']),
    url('/forums/thread/<thread_id>/move/', view_func=views.forums_thread_move,
        name='forum_thread_move', methods=['POST'])
]
