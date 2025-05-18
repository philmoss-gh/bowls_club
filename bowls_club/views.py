from django.shortcuts import render, get_object_or_404
from .models import Competition, Match

# filepath: c:\Users\Phil\Desktop\Dev\bowls_club\views.py

def index(request):
    return render(request, 'master.html')  # Render the master.html template

def home(request):
    return render(request, 'home.html')  # Render the home.html template

def players(request):
    return render(request, 'players.html')  # Render the players.html template

def competitions(request):
    competitions = Competition.objects.all()  # Fetch all competitions from the database
    return render(request, 'competitions.html', {'competitions': competitions})

def sponsors(request):  
    return render(request, 'sponsors.html')  # Render the sponsors.html template

def fixtures_results(request, competition_id):
    competition = get_object_or_404(Competition, id=competition_id)
    matches = Match.objects.filter(competition=competition)  # Fetch all matches for the competition
    return render(request, 'fixtures_results.html', {'competition': competition, 'matches': matches})