from unicodedata import name
from django.urls import path

from . import views

urlpatterns = [
    path("", views.signup, name="signup"),
    path("login/", views.loginpage, name="login")
    # path("wiki/<str:name>", views.greet, name = "greet"), 
    # path("search/", views.search, name = "search"),
    # path("new_page/", views.new_page, name="new_page"),
    # path("random/", views.random_, name="random"), 
    # path("edit/<str:title>", views.edit_page, name = "edit"), 
    # path("login/", views.login, name = "login"),
]
