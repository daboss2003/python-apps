from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_listing", views.new_listing, name="new_listing"),
    path("listing_page/<int:listing_id>",views.listing_page,name="listing_page"),
    path("comment/<int:listing_id>",views.comment,name="comment"),
    path("add_to_wishlist/<int:listing_id>",views.add_to_wishlist,name="add_to_wishlist"),
    path("close_listing/<int:listing_id>",views.close_listing,name="close_listing"),
    path("wish_list_page",views.wish_list_page,name="wish_list_page"),
    path("view_categories",views.view_categories,name="view_categories"),
    path("display_category/<int:category_id>",views.display_category,name="display_category")
]
