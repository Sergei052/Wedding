from django.contrib import admin
from django.urls import path
from rsvp.views import invitation

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', invitation, name='invitation'),
]