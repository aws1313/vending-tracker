from django.urls import path
from vt_public_web import views
urlpatterns = [
    path("", views.index, name="index"),

    path("feedback", views.feedback, name="vt_public_web_feedback"),
]