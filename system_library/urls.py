# Importing required libraries
from django.urls import path
from . import views


# Url patterns for Books app module of Library Management System
urlpatterns = [
    path("", views.home, name="home"),
    path("bookadd", views.add_book_isbn, name=""),
    path("bookupdate", views.update_book_isbn, name=""),
    path("bookdelete", views.delete_book_isbn, name=""),
    path("bookquery", views.query_book, name=""),
    path("bookqueryAll", views.query_book_all, name=""),
    path("lend", views.lend_book, name=""),
    path("issue", views.issue, name="issue"),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("logout", views.logout, name="logout"),
    path("return_item", views.return_item, name="return_item"),
    path("history", views.history, name="history"),
]