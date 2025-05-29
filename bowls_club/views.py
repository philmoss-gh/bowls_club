from django.shortcuts import render, get_object_or_404, redirect
from .models import Competition, Match, Member, Sponsor, MatchAvailability
from django.db.models import Case, When, Value, IntegerField
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import timezone
import json
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm, CustomUserCreationForm
from django.contrib.auth.decorators import login_required

# filepath: c:\Users\Phil\Desktop\Dev\bowls_club\views.py

def index(request):
    return render(request, 'master.html')  # Render the master.html template

def home(request):
    return render(request, 'home.html')  # Render the home.html template

def players(request):
    role_order = Case(
        When(role='Captain', then=Value(0)),
        When(role='Vice-Captain', then=Value(1)),
        When(role='Player', then=Value(2)),
        When(role='Social', then=Value(3)),
        default=Value(4),
        output_field=IntegerField(),
    )
    members = Member.objects.all().order_by('team', role_order, 'last_name', 'first_name')
    # Change 'Social' to 'Socialites' for display
    teams = ['Ladies', 'Men', 'Socialites']
    # Optionally, map 'Social' team members to 'Socialites' for display
    for m in members:
        if m.team == 'Social':
            m.team = 'Socialites'
    return render(request, 'players.html', {'members': members, 'teams': teams})

def competitions(request):
    competitions = Competition.objects.all()
    return render(request, 'competitions.html', {'competitions': competitions})

def sponsors(request):  
    sponsors = Sponsor.objects.all()
    return render(request, 'sponsors.html', {'sponsors': sponsors})

def fixtures_results(request, competition_id):
    competition = get_object_or_404(Competition, pk=competition_id)
    matches = competition.matches.all()

    # Get filter parameters from GET request
    selected_competition = request.GET.get('competition')
    selected_year = request.GET.get('year')

    # Filter by competition if provided
    if selected_competition:
        matches = matches.filter(competition__id=selected_competition)

    # Filter by year if provided
    if selected_year:
        matches = matches.filter(date__year=selected_year)

    # For year dropdown/filter
    years = matches.dates('date', 'year')
    # For competition dropdown/filter
    competitions = Competition.objects.all()

    # Remove 'Bowls Club' from opposition team name for display
    match_list = []
    for match in matches.order_by('date'):  # Order by date ascending
        opp_name = match.opposition_team.name
        opp_name = opp_name.replace('Bowls Club', '').replace('bowls club', '').replace('Bowls club', '').replace('bowls Club', '').strip()
        available = False
        if request.user.is_authenticated:
            available = MatchAvailability.objects.filter(match=match, user=request.user, available=True).exists()
        match_list.append({
            "id": match.id,
            "date": match.date,
            "opposition": opp_name,
            "home_or_away": match.home_or_away,
            "our_score": match.our_score,
            "their_score": match.their_score,
            "competition_name": match.competition.name,
            "available": available,
        })

    return render(request, "fixtures_results.html", {
        "competition": competition,
        "matches": match_list,
        "years": years,
        "competitions": competitions,
        "selected_competition": selected_competition,
        "selected_year": selected_year,
    })

def member_profile(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    return render(request, 'member_profile.html', {'member': member})

def contact(request):
    sent = False
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # Send email (or save to DB if you prefer)
            send_mail(
                subject=f"Contact Form: {form.cleaned_data['name']}",
                message=form.cleaned_data['message'],
                from_email=form.cleaned_data['email'],
                recipient_list=[settings.DEFAULT_FROM_EMAIL],  # Set this in your settings.py
            )
            sent = True
    else:
        form = ContactForm()
    return render(request, "contact.html", {"form": form, "sent": sent})

@login_required
def members_area(request):
    return render(request, "members_area.html")

@login_required
def update_availability(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    if request.method == "POST":
        available = request.POST.get("availability") == "yes"
        MatchAvailability.objects.update_or_create(
            match=match,
            user=request.user,
            defaults={"available": available}
        )
    return redirect('fixtures_results', competition_id=match.competition.id)

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/register.html", {"form": form})



