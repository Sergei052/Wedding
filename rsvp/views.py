from django.shortcuts import render,redirect
from .forms import RSVPForm

def invitation(request):
    if request.method == 'POST':
        form = RSVPForm(request.POST)
        if form.is_valid():
            rsvp = form.save()
            request.session['rsvp_attending'] = rsvp.attending
            return redirect('invitation')
    else:
        form = RSVPForm()

    attending = request.session.pop('rsvp_attending', None)
    return render(request, 'rsvp/invitation.html', {
        'form': form,
        'success': attending is not None,
        'attending': attending,
    })