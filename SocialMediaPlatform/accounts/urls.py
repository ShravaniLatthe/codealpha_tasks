from django.urls import path
from . import views

urlpatterns = [

    path("register/", views.register, name="register"),

    path("login/", views.login_user, name="login"),

    path("logout/", views.logout_user, name="logout"),

    path("profile/", views.profile, name="profile"),

    path("edit-profile/", views.edit_profile, name="edit_profile"),
    path(
    "user/<str:username>/",
    views.user_profile,
    name="user_profile"
),
path(
    "search/",
    views.search_users,
    name="search_users"
),
path(
    "follow/<str:username>/",
    views.follow_user,
    name="follow_user"
),
]