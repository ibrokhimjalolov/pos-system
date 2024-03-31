from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path("", include("pos_system.urls", namespace="pos_system")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
