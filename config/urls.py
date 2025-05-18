from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('bowls_club/', include('bowls_club.urls')),  # Include bowls_club URLs
]