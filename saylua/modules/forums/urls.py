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
    url('/forums/', view_func=views.forums_home, name='home'),
    url('/forums/board/<canon_name>/', view_func=views.forums_board,
        name='board', methods=['GET', 'POST']),

    # Stuff you can do while viewing a forum thread.
    url('/forums/thread/<thread>/', view_func=views.forums_thread,
        name='thread', methods=['GET', 'POST']),
    url('/forums/thread/<thread>/<int:page>/', view_func=views.forums_thread,
        name='thread', methods=['GET', 'POST']),

    url('/forums/thread/move/<int:thread_id>/', view_func=views.forums_thread_move,
        name='thread_move', methods=['POST']),
    url('/forums/thread/pin/<int:thread_id>/', view_func=views.forums_thread_pin,
        name='thread_pin', methods=['POST']),
    url('/forums/thread/lock/<int:thread_id>/', view_func=views.forums_thread_lock,
        name='thread_lock', methods=['POST']),

    url('/forums/thread/subscribe/<int:thread_id>/', view_func=views.forums_thread_subscribe,
        name='thread_subscribe', methods=['POST']),

    url('/forums/post/edit/<int:post_id>/', view_func=views.forums_post_edit,
        name='post_edit', methods=['GET', 'POST'])
]
