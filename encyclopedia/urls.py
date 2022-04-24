from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.display_contents, name="md-entry"),
    path("newpage", views.new_page, name="new_page"),
    path("randompage", views.random_page, name="random_page"),
]
