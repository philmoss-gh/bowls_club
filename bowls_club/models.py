from django.db import models
from django.core.exceptions import ValidationError


class Competition(models.Model):
    COMPETITION_TYPES = [
        ('knockout', 'Knockout'),  # Knockout competition type
        ('league', 'League'),  # League competition type
        ('friendly', 'Friendly'),  # Friendly competition type
        ('tournament', 'Tournament'),  # Tournament competition type
    ]

    name = models.CharField(max_length=255)  # Name of the competition
    competition_type = models.CharField(
        max_length=50,
        choices=COMPETITION_TYPES,
        default='knockout',  # Default competition type
    )

    def __str__(self):
        return self.name  # String representation of the competition


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

    first_name = models.CharField(max_length=50)  # First name of the member
    last_name = models.CharField(max_length=50)  # Last name of the member
    team = models.CharField(max_length=6, choices=TEAM_CHOICES)  # Team choice: Men, Ladies, or Social
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default='Player')  # Role choice: Captain, Vice-Captain, Player, or Social
    email = models.EmailField()  # Email address of the member
    phone = models.CharField(max_length=15)  # Phone number of the member

    def save(self, *args, **kwargs):
        # Set role to "Social" if team is "Social"
        if self.team == 'Social':
            self.role = 'Social'
        super().save(*args, **kwargs)  # Call the parent class's save method

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"  # String representation of the member


class Rink(models.Model):
    number = models.IntegerField()  # Rink number
    players = models.ManyToManyField(Member, related_name="rinks", blank=True)  # Members assigned to the rink
    match = models.OneToOneField('Match', on_delete=models.CASCADE, related_name="rink", blank=True, null=True)  # Match assigned to the rink

    def clean(self):
        if self.players.count() > 4:
            raise ValidationError("A rink can have a maximum of 4 players.")

    def __str__(self):
        return f"Rink {self.number}"  # String representation of the rink


class Sponsor(models.Model):
    name = models.CharField(max_length=255)  # Name of the sponsor
    logo = models.ImageField(upload_to='sponsor_logos/')  # Logo of the sponsor
    website = models.URLField()  # Website of the sponsor

    def __str__(self):
        return self.name  # String representation of the sponsor


class MembershipPayment(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="payments")  # Link to the Member model
    date = models.DateField()  # Date of the payment
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Payment amount

    def __str__(self):
        return f"Payment of {self.amount} by {self.member.first_name} {self.member.last_name} on {self.date}"


class OppositionTeam(models.Model):
    name = models.CharField(max_length=255)  # Name of the opposition team
    location = models.CharField(max_length=255, blank=True, null=True)  # Location of the opposition team
    contact_email = models.EmailField(blank=True, null=True)  # Contact email for the opposition team
    contact_phone = models.CharField(max_length=15, blank=True, null=True)  # Contact phone number for the opposition team
    competitions = models.ManyToManyField(Competition, related_name="opposition_teams", blank=True)  # Competitions the team participates in

    def __str__(self):
        return self.name  # String representation of the opposition team


class Match(models.Model):
    HOME_OR_AWAY_CHOICES = [
        ('Home', 'Home'),
        ('Away', 'Away'),
    ]

    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)  # Competition the match belongs to
    date = models.DateTimeField()  # Date and time of the match
    home_or_away = models.CharField(max_length=4, choices=HOME_OR_AWAY_CHOICES, default='Home')  # Home or Away
    opposition_team = models.ForeignKey(OppositionTeam, on_delete=models.CASCADE, related_name="matches_as_opposition")  # Opposition team
    crosshands_score = models.IntegerField(blank=True, null=True)  # Score of the home team (optional)
    opposition_score = models.IntegerField(blank=True, null=True)  # Score of the away team (optional)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Call the parent class's save method

    def __str__(self):
        if self.home_or_away == 'Home':
            return f"Crosshands vs {self.opposition_team.name} - {self.competition.name}"  # Home game
        else:
            return f"{self.opposition_team.name} vs Crosshands - {self.competition.name}"  # Away game


class OwnClub(models.Model):
    name = models.CharField(max_length=255)  # Name of the club
    short_name = models.CharField(max_length=50)  # Short name of the club
    location = models.CharField(max_length=255)  # Location of the club
    contact_email = models.EmailField(blank=True, null=True)  # Contact email for the club
    contact_phone = models.CharField(max_length=15, blank=True, null=True)  # Contact phone number for the club
    website = models.URLField(blank=True, null=True)  # Website of the club
    established_year = models.IntegerField(blank=True, null=True)  # Year the club was established

    def __str__(self):
        return self.name  # String representation of the club