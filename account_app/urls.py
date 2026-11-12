from django.urls import path

from . import views

urlpatterns = [
    # Authentification
    path("register-user/", views.register_user, name="register_user"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    
    # activer le compte par mail
    path("activate/<uidb64>/<token>", views.activate, name="activate"),
    
    # user profile --> simulation paiament
    path("list-profile", views.list_profile, name="list_profile"),
    
    # user list
    path("list-user", views.user_list, name="user_list"),
]
