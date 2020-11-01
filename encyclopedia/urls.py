from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>", views.viewpage, name="viewpage"),
    path("search", views.search, name="search"),
    path("randompage", views.randompage, name="randompage"),
    path("newpage", views.newpage, name="newpage"),
    path("edit/<str:name>", views.editpage, name="edit")
]
