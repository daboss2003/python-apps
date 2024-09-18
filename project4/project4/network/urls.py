
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("get_profile/<int:user_id>",views.get_profile,name="get_profile"),
    path("create_user_post",views.create_user_post,name="create_user_post"),
    path("get_post/<int:post_id>",views.get_post,name="get_post"),
    path("get_like/<int:post_id>",views.get_like,name="get_like"),
    path("get_comment/<int:post_id>",views.get_comment,name="get_comment"),
    path("get_notification",views.get_notification,name="get_notification"),
    path("get_all_user",views.get_all_user,name="get_all_user"),
    path("edit_post/<int:post_id>",views.edit_post,name="edit_post"),
    path("edit_profile",views.edit_profile,name="edit_profile"),
    path("get_friends_post",views.get_friends_post,name="get_friends_post"),
    path("send_friend_request/<int:friend_id>",views.send_friend_request,name="send_friend_request"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    


    
