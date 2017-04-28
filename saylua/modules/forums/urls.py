from saylua.routing import url
from . import admin_views
from . import views


urlpatterns = [
    # Admin Views
    url('/admin/forums/newboard/', view_func=admin_views.new_board,
        name='admin_new_board', methods=['GET', 'POST']),
    url('/admin/forums/newcategory/', view_func=admin_views.new_board_category,
        name='admin_new_category', methods=['GET', 'POST']),

    # Primary Views
    url('/forums/', view_func=views.forums_home, name='forum_home'),
    url('/forums/board/<canon_name>/', view_func=views.forums_board,
        name='forum_board', methods=['GET', 'POST']),
    url('/forums/thread/<thread_id>/', view_func=views.forums_thread,
        name='forum_thread', methods=['GET', 'POST']),
    url('/forums/thread/<thread_id>/move/', view_func=views.forums_thread_move,
        name='forum_thread_move', methods=['POST'])
]
