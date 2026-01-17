"""
URL configuration for vt_conf project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from xml.etree.ElementInclude import include

from django.contrib import admin
from allauth.account.decorators import secure_admin_login
from django.urls import path, include
from vt_conf import views
from django.conf import settings
from django.conf.urls.static import static

admin.autodiscover()
admin.site.login = secure_admin_login(admin.site.login)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path("", include("vt_public_web.urls")),

    path("api/", include("vt_api.urls")),

    path("dashboard/", include("vt_products.urls"))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

