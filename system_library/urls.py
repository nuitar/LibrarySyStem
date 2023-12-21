# Importing required libraries
from django.urls import path
from . import views


# Url patterns for Books app module of Library Management System
urlpatterns = [
    path("", views.home, name="home"),
    path("book_add", views.add_book, name="book_add"),
    path("book_update", views.update_book_isbn, name="book_update"),
    path("book_delete", views.delete_book_isbn, name="book_delete"),
    path("book_query", views.query_book, name="book_query"),
    path("book_query_All", views.query_book_all, name="book_queryAll"),
    
    path("person_query", views.query_person, name="person_query"),
    path("person_query_lend", views.person_query_lend, name="person_query_lend"),
    path("person_add", views.add_person, name="person_add"),
    
    path("lend_query_all", views.query_lend_all, name="lend_query_all"),
    path("lend", views.lend_book, name="lend"),
    path("return", views.return_book, name="return"),
    
    
    path("img/read/<str:img_name>", views.img_read, name="img"),
    path("img/save/<str:img_name>", views.img_save, name="img"),
    
    path("issue", views.issue, name="issue"),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("logout", views.logout, name="logout"),
    path("return_item", views.return_item, name="return_item"),
    path("history", views.history, name="history"),
]