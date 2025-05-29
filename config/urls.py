from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from bowls_club import views  # <-- add this import

urlpatterns = [
    path('admin/', admin.site.urls),
    path('bowls_club/', include('bowls_club.urls')),
    path('accounts/', include('django.contrib.auth.urls')),  # <-- Add this line

    path('', views.home, name='home'),  # <-- add this line for root URL
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)