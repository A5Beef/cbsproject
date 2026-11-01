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
]
