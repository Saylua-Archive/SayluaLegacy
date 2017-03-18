from saylua.routing import url
import views


urlpatterns = [
    # Messages
    url('/messages/', view_func=views.messages.messages_main, name="messages"),
    url('/messages/', view_func=views.messages.messages_main_post,
        name="messages_post", methods=['POST']),
    url('/messages/write/', view_func=views.messages.messages_write_new,
        name="messages_write", methods=['GET', 'POST']),
    url('/conversation_read/<key>/', view_func=views.messages.messages_read,
        name="messages_read"),
    url('/conversation/<key>/', view_func=views.messages.messages_view_conversation,
        name="messages_view_conversation", methods=['GET', 'POST']),

    # Notifications
    url('/notifications/', view_func=views.notifications.notifications_main,
        name="notifications"),
    url('/notifications/', view_func=views.notifications.notifications_main_post,
        name="notifications_post", methods=['POST']),
    url('/notification/<key>/', view_func=views.notifications.notification_follow,
        name="notifications_follow")
]
