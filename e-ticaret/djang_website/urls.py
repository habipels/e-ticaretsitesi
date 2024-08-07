"""django_website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404
from django.views.generic.base import TemplateView #import TemplateView

urlpatterns = [
    path("", include('main.urls')),
    path('admin/', admin.site.urls),
    path("yonetim/",include("admin_page.urls")),
    path('users/',include("users.urls", namespace='users')),
    path('pay/', include('odeme_kisimlari.urls',namespace='pay')),
    path("robots.txt",TemplateView.as_view(template_name="robot.txt", content_type="text/plain")),  #add the robots.txt file
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
handler404 = "main.views.page_not_found_view"