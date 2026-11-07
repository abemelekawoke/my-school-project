from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework import routers
import requests
from rest_framework_simplejwt import views as jwt_views
# Customize Django admin branding
admin.site.site_header = "King's 🏫 Academy Solutions"
admin.site.site_title = "King's Academy Solutions Portal"
admin.site.index_title = "Welcome to the King's Academy Dashboard"
from django.conf import settings

from django.conf.urls.static import static
# from student.views import dashboard_view
# from student.views import custom_admin_index
# from setups.admin import custom_admin_site

urlpatterns = [
    path('admin/', admin.site.urls),  # Default Django admin
    # path('admin/', custom_admin_index),  # ✅ override index view only
    # path("admin/", custom_admin_site.urls),   # ✅ must be this
    path("i18n/", include("django.conf.urls.i18n")),  # Add this line
    path('chaining/', include('smart_selects.urls')),
    path('humanresource/', include('humanresource.urls')),  # Include employees URLs here
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
