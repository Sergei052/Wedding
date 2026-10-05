from django.shortcuts import render
from .forms import RSVPForm

def invitation(request):
    success = False
    attending = None

    if request.method == 'POST':
        form = RSVPForm(request.POST)
        if form.is_valid():
            rsvp = form.save()
            success = True
            attending = rsvp.attending
    else:
        form = RSVPForm()

    return render(request, 'rsvp/invitation.html', {
        'form': form,
        'success': success,
        'attending': attending
    })