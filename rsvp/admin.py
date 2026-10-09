from django.contrib import admin
from .models import RSVP

@admin.register(RSVP)
class RSVPAdmin(admin.ModelAdmin):
    list_display = ('name', 'attending','coming_alone', 'has_companion', 'created_at')
    list_filter = ('attending', 'created_at')
    search_fields = ('name',)
    readonly_fields = ('created_at',)