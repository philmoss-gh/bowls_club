# filepath: c:\Users\Phil\Desktop\Dev\bowls_club\urls.py
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),  # Default view for bowls_club
    path('home/', views.home, name='home'),  # Home page
    path('players/', views.players, name='players'),  # Players page
    path('competitions/', views.competitions, name='competitions'),  # Competitions page
    path('sponsors/', views.sponsors, name='sponsors'),  # Sponsors page
    path('fixtures_results/<int:competition_id>/', views.fixtures_results, name='fixtures_results'),  # Fixtures and Results page
    path('member/<int:member_id>/', views.member_profile, name='member_profile'),  # Member profile page
    path('contact/', views.contact, name='contact'),  # Contact page
    path('members/', views.members_area, name='members_area'),
    path('accounts/', include('django.contrib.auth.urls')),  # login/logout/password
    path('match/<int:match_id>/availability/', views.update_availability, name='update_availability'),    
    path('register/', views.register, name='register'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)