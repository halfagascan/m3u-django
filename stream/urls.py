from django.urls import path
from django.conf.urls.static import static
from . import views
from django.conf import settings
from .views import test_public
from .views import m3u  # Adjust the import if needed

urlpatterns = [
    path('channels/', views.m3u, name='index'),
    path('epg/', views.epg, name='index'),
    path('testpublic/', test_public),
    path('citrus.m3u', m3u, name='citrus_m3u'),
    path('citrus.xml', views.epg, name='citrus_xml'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
