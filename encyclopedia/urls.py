from django.urls import path
from . import views
from . import util

urlpatterns = [
    path("", views.index, name="index or home"),
    path("createpage/", views.create_new_page, name="create new page"),
    path("randompage/", views.random_page, name="random page"),
    path("<str:entry>/", views.load_page, name="specific entry"),

]
