from django.urls import path
from vt_public_web import views
urlpatterns = [
    path("", views.index, name="index"),
    path("impressum", views.impressum, name="impressum"),
]