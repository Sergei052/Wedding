from django.contrib import admin

from .models import RSVP


@admin.register(RSVP)
class RSVPAdmin(admin.ModelAdmin):
    list_display = ('name', 'attending', 'has_companion', 'created_at')
    list_filter = ('attending', 'has_companion', 'created_at')
    search_fields = ('name',)
    readonly_fields = ('created_at',)
    list_per_page = 100