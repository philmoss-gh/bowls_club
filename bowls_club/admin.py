from django.contrib import admin
from django import forms
from .models import Competition, Member, Rink, Match, Sponsor, MembershipPayment, OppositionTeam, OwnClub, MatchAvailability
from django.contrib.auth.models import User

class MembershipPaymentInline(admin.TabularInline):
    model = MembershipPayment
    extra = 1  # Number of empty forms to display for adding new payments

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'team', 'role')  # Display these fields in the admin list view
    search_fields = ('first_name', 'last_name')
    inlines = [MembershipPaymentInline]  # Add the inline payments to the Member admin

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj and obj.team == 'Social':  # If editing an existing object and team is 'Social'
            form.base_fields['role'].initial = 'Social'
        return form

class RinkInlineForm(forms.ModelForm):
    class Meta:
        model = Rink
        exclude = ('players',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        match = None
        # Get the match instance from the parent object if available
        if self.instance and self.instance.match_id:
            match = self.instance.match
        elif 'initial' in kwargs and 'match' in kwargs['initial']:
            match = kwargs['initial']['match']
        # If editing an existing match, filter by availability for that match
        if match:
            available_user_ids = MatchAvailability.objects.filter(
                match=match, available=True
            ).values_list('user_id', flat=True)
            available_user_emails = User.objects.filter(
                id__in=available_user_ids
            ).values_list('email', flat=True)
            available_members = Member.objects.filter(
                email__in=available_user_emails
            )
            self.fields['lead'].queryset = available_members
            self.fields['second'].queryset = available_members
            self.fields['third'].queryset = available_members
            self.fields['skip'].queryset = available_members
        else:
            # If no match context, show all members
            qs = Member.objects.all().order_by('last_name', 'first_name')
            self.fields['lead'].queryset = qs
            self.fields['second'].queryset = qs
            self.fields['third'].queryset = qs
            self.fields['skip'].queryset = qs

class RinkInline(admin.TabularInline):  # or admin.StackedInline for a different style
    model = Rink
    form = RinkInlineForm
    extra = 4  # Show 4 empty forms by default

    def get_formset(self, request, obj=None, **kwargs):
        # Pass the match instance to the form via kwargs
        FormSet = super().get_formset(request, obj, **kwargs)
        class InlineFormSet(FormSet):
            def _construct_form(self, i, **kwargs):
                if obj:
                    kwargs['initial'] = kwargs.get('initial', {})
                    kwargs['initial']['match'] = obj
                return super()._construct_form(i, **kwargs)
        return InlineFormSet

class MatchAdmin(admin.ModelAdmin):
    list_display = (
        'competition',
        'date',
        'get_away_team',
        'home_or_away',
        'our_score',
        'their_score',
    )
    list_filter = ('competition', 'date', 'home_or_away')  # Add filters for competition, date, and home/away
    search_fields = ('opposition_team__name', 'competition__name')  # Enable search by opposition team and competition names
    inlines = [RinkInline]  # <-- Now this works!

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

class RinkAdminForm(forms.ModelForm):
    class Meta:
        model = Rink
        # Exclude the players field from the form
        exclude = ('players',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Order player dropdowns alphabetically by last name, then first name
        qs = Member.objects.all().order_by('last_name', 'first_name')
        self.fields['lead'].queryset = qs
        self.fields['second'].queryset = qs
        self.fields['third'].queryset = qs
        self.fields['skip'].queryset = qs

class RinkAdmin(admin.ModelAdmin):
    form = RinkAdminForm
    filter_horizontal = ('players',)

    class Media:
        css = {
            'all': ('bowls_club/admin_extra.css',)
        }

@admin.register(MatchAvailability)
class MatchAvailabilityAdmin(admin.ModelAdmin):
    list_display = ('user', 'match', 'available')
    list_filter = ('available', 'match')
    search_fields = ('user__username', 'match__id')



# Register the models with the admin site
admin.site.register(Match, MatchAdmin)
admin.site.register(Competition)
admin.site.register(Rink, RinkAdmin)
admin.site.register(Sponsor)
admin.site.register(MembershipPayment)  # Register MembershipPayment separately
admin.site.register(OppositionTeam, OppositionTeamAdmin)  # Register the customized OppositionTeam admin
admin.site.register(OwnClub, OwnClubAdmin)  # Register the customized OwnClub admin

# Customize the admin site header
admin.site.site_header = "Crosshands Bowls Admin"
admin.site.site_title = "Crosshands Bowls Admin Portal"
admin.site.index_title = "Welcome to Crosshands Bowls Admin"