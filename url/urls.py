from django.urls import path
from . import views
app_name = "url"
urlpatterns = [
    path("", views.url_short, name="home"),
    path("u/<str:slugs>", views.url_redirect, name="redirect")
]