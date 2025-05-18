# filepath: c:\Users\Phil\Desktop\Dev\bowls_club\urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Default view for bowls_club
    path('home/', views.home, name='home'),  # Home page
    path('players/', views.players, name='players'),  # Players page
    path('competitions/', views.competitions, name='competitions'),  # Competitions page
    path('sponsors/', views.sponsors, name='sponsors'),  # Sponsors page
    path('fixtures_results/<int:competition_id>/', views.fixtures_results, name='fixtures_results'),  # Fixtures and Results page
]