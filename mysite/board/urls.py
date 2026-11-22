from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path("register/", views.register, name="register"),

    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="board/login.html"
        ),
        name="login"
    ),

    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout"
    ),

    path(
        "create/",
        views.create_thread,
        name="create_thread"
    ),

    path(
        "thread/<int:thread_id>/",
        views.thread_detail,
        name="thread_detail"
    ),

    path("thread/<int:thread_id>/reply/",
        views.create_reply,
        name="create_reply"
        ),

    path("thread/<int:thread_id>/post/<int:post_id>/edit/",
        views.edit_post,
        name="edit_post"
        ),

    path("thread/<int:thread_id>/post/<int:post_id>/delete/",
        views.delete_post,
        name="delete_post"
        ),

    path("inbox/",
        views.inbox,
        name="inbox"
        ),

    path("messages/sent/",
        views.sent_messages,
        name="sent_messages"
        ),

    path("message/send/",
        views.send_message,
        name="send_message"
        ),

    path("message/<int:message_id>/",
        views.message_detail,
        name="message_detail"
        ),
]
