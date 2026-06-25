from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("create-post/", views.create_post, name="create_post"),
    path("like/<int:post_id>/", views.like_post, name="like_post"),
    path("comment/<int:post_id>/",views.add_comment,name="add_comment"),
    path(
    "edit-post/<int:post_id>/",
    views.edit_post,
    name="edit_post"
),
    path(
    "delete-post/<int:post_id>/",
    views.delete_post,
    name="delete_post"
),
]