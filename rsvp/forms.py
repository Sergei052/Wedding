from django import forms
from .models import RSVP

class RSVPForm(forms.ModelForm):
    attending = forms.TypedChoiceField(
        choices=[(True, 'Да, я буду'), (False, 'К сожалению, не смогу')],
        widget=forms.RadioSelect,
        coerce=lambda x: x == 'True',
        label='Вы будете на свадьбе?'
    )
    coming_alone = forms.TypedChoiceField(
        choices=[(True, 'Да'), (False, 'Нет')],
        widget=forms.RadioSelect,
        coerce=lambda x: x == 'True',
        label='Вы придёте один/одна?'
    )

    has_companion = forms.TypedChoiceField(
        choices=[(True, 'Да'), (False, 'Нет')],
        widget=forms.RadioSelect,
        coerce=lambda x: x == 'True',
        label='С вами будет сопровождающий?'
    )
    class Meta:
        model = RSVP
        fields = ['name', 'attending', 'coming_alone', 'has_companion']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Ваше имя'
            }),
        }
        labels = {
            'name': '',
        }

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if RSVP.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError('Это имя уже использовано. Если вы уже отвечали — повторно отправлять не нужно.')
        return name