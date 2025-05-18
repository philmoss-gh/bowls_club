from django.contrib import admin
from .models import Competition, Member, Rink, Match, Sponsor, MembershipPayment, OppositionTeam, OwnClub

class MembershipPaymentInline(admin.TabularInline):
    model = MembershipPayment
    extra = 1  # Number of empty forms to display for adding new payments

class MemberAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'team', 'role')  # Display these fields in the admin list view
    inlines = [MembershipPaymentInline]  # Add the inline payments to the Member admin

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj and obj.team == 'Social':  # If editing an existing object and team is 'Social'
            form.base_fields['role'].initial = 'Social'
        return form

class MatchAdmin(admin.ModelAdmin):
    list_display = ('competition', 'date', 'get_away_team', 'home_or_away', 'crosshands_score', 'opposition_score')  # Display these fields in the admin list view
    list_filter = ('competition', 'date', 'home_or_away')  # Add filters for competition, date, and home/away
    search_fields = ('opposition_team__name', 'competition__name')  # Enable search by opposition team and competition names

    # Custom method to display the away team name
    def get_away_team(self, obj):
        return obj.opposition_team.name  # Return the name of the opposition team
    get_away_team.short_description = 'Opposition'

class OwnClubAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'contact_email', 'contact_phone', 'website', 'established_year')  # Display these fields in the admin list view
    search_fields = ('name', 'location', 'contact_email')  # Enable search by name, location, and email
    list_filter = ('established_year',)  # Add a filter for the established year
    fieldsets = (
        (None, {
            'fields': ('name', 'location', 'contact_email', 'contact_phone', 'website', 'established_year')
        }),
    )  # Organize fields into sections

    # Restrict adding new entries if one already exists
    def has_add_permission(self, request):
        if OwnClub.objects.exists():
            return False  # Disable the "Add" button if an entry already exists
        return True

    # Restrict deleting entries
    def has_delete_permission(self, request, obj=None):
        return False  # Disable the "Delete" button

class OppositionTeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_competitions')  # Display these fields in the admin list view
    search_fields = ('name', 'location', 'contact_email')  # Enable search by name, location, and email
    list_filter = ('competitions',)  # Add a filter for competitions
    filter_horizontal = ('competitions',)  # Use a horizontal filter widget for the ManyToManyField
    fieldsets = (
        (None, {
            'fields': ('name', 'location', 'contact_email', 'contact_phone', 'competitions')  # Include competitions in the form
        }),
    )  # Organize fields into sections

    # Custom method to display competitions as a comma-separated list
    def get_competitions(self, obj):
        return ", ".join([competition.name for competition in obj.competitions.all()])
    get_competitions.short_description = 'Competitions'

# Register the models with the admin site
admin.site.register(Match, MatchAdmin)
admin.site.register(Competition)
admin.site.register(Member, MemberAdmin)  # Use the customized MemberAdmin
admin.site.register(Rink)
admin.site.register(Sponsor)
admin.site.register(MembershipPayment)  # Register MembershipPayment separately
admin.site.register(OppositionTeam, OppositionTeamAdmin)  # Register the customized OppositionTeam admin
admin.site.register(OwnClub, OwnClubAdmin)  # Register the customized OwnClub admin

# Customize the admin site header
admin.site.site_header = "Crosshands Bowls Admin"
admin.site.site_title = "Crosshands Bowls Admin Portal"
admin.site.index_title = "Welcome to Crosshands Bowls Admin"