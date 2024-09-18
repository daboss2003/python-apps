from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:name>", views.entry_name, name="entry_name"),
    path("/search", views.search, name="search"),
    path("/create_new",views.create_new, name="create_new"),
    path("edit_page/<str:name>", views.edit_page, name="edit_page"),
    path("/random_page", views.random_page, name="random_page")
]
