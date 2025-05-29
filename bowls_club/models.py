from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class Competition(models.Model):
    name = models.CharField(max_length=255)
    competition_type = models.CharField(
        max_length=50,
        choices=[
            ('knockout', 'Knockout'),
            ('league', 'League'),
            ('friendly', 'Friendly'),
            ('tournament', 'Tournament'),
        ],
        default='knockout',
    )

    def __str__(self):
        return self.name


class Member(models.Model):
    TEAM_CHOICES = [
        ('Men', 'Men'),
        ('Ladies', 'Ladies'),
        ('Social', 'Social'),
    ]
    ROLE_CHOICES = [
        ('Captain', 'Captain'),
        ('Vice-Captain', 'Vice-Captain'),
        ('Player', 'Player'),
        ('Social', 'Social'),
    ]
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    team = models.CharField(max_length=20, choices=TEAM_CHOICES)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Player')
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    profile_text = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='member_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Sponsor(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='sponsor_logos/')
    website = models.URLField()
    profile = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def image(self):
        return self.logo

    def as_dict(self):
        return {
            "name": self.name,
            "image": self.logo.url if self.logo else "",
            "profile": self.profile,
            "website": self.website,
        }

class MembershipPayment(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="payments")
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Payment of {self.amount} by {self.member.first_name} {self.member.last_name} on {self.date}"

class OppositionTeam(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    contact_phone = models.CharField(max_length=15, blank=True, null=True)
    competitions = models.ManyToManyField(Competition, related_name="opposition_teams", blank=True)

    def __str__(self):
        return self.name

class Match(models.Model):
    HOME_OR_AWAY_CHOICES = [
        ('Home', 'Home'),
        ('Away', 'Away'),
    ]
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='matches')
    date = models.DateTimeField()
    home_or_away = models.CharField(max_length=4, choices=HOME_OR_AWAY_CHOICES, default='Home')
    opposition_team = models.ForeignKey(OppositionTeam, on_delete=models.CASCADE, related_name='matches')
    our_score = models.IntegerField(blank=True, null=True)
    their_score = models.IntegerField(blank=True, null=True)

    def __str__(self):
        if self.home_or_away == 'Home':
            return f"Crosshands vs {self.opposition_team.name} - {self.competition.name}"
        else:
            return f"{self.opposition_team.name} vs Crosshands - {self.competition.name}"

class Rink(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='rinks')
    number = models.PositiveIntegerField()

    # Add explicit player positions
    lead = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name='rinks_as_lead', null=True, blank=True)
    second = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name='rinks_as_second', null=True, blank=True)
    third = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name='rinks_as_third', null=True, blank=True)
    skip = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name='rinks_as_skip', null=True, blank=True)

    players = models.ManyToManyField(Member, related_name='rinks', blank=True)  # Optional: keep for legacy/multi-player support

    def __str__(self):
        return f"Rink {self.number} for {self.match}"

class OwnClub(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    contact_email = models.EmailField(blank=True, null=True)
    contact_phone = models.CharField(max_length=15, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    established_year = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name

class MatchAvailability(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    available = models.BooleanField(default=False)

    class Meta:
        unique_together = ('match', 'user')

    def __str__(self):
        return f"{self.user.username} - {self.match} - {'Available' if self.available else 'Not Available'}"