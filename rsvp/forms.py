from django import forms

from .models import RSVP

YES_NO = [(True, 'Да'), (False, 'Нет')]


def to_bool(value):
    return value == 'True'


class RSVPForm(forms.ModelForm):
    attending = forms.TypedChoiceField(
        choices=[(True, 'Да, я буду'), (False, 'К сожалению, не смогу')],
        widget=forms.RadioSelect,
        coerce=to_bool,
        label='Вы будете на свадьбе?',
        error_messages={'required': 'Выберите один из вариантов.'},
    )
    has_companion = forms.TypedChoiceField(
        choices=[(False, 'Нет, приду один/одна'), (True, 'Да, будет сопровождающий')],
        widget=forms.RadioSelect,
        coerce=to_bool,
        empty_value=False,
        required=False,
        initial=False,
        label='Будет ли с вами сопровождающий?',
    )

    class Meta:
        model = RSVP
        fields = ['name', 'attending', 'has_companion']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Ваше имя ..',
                'autocomplete': 'name',
                'maxlength': '100',
            }),
        }
        labels = {'name': 'Как вас зовут? '}
        error_messages = {
            'name': {'required': 'Напишите, пожалуйста, ваше имя.'},
        }

    def clean_name(self):
        name = ' '.join(self.cleaned_data.get('name', '').split())
        if RSVP.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError(
                'Это имя уже использовано. Если вы уже отвечали — повторно отправлять не нужно.'
            )
        return name

    def clean(self):
        data = super().clean()
        # Тот, кто не придёт, без сопровождающего
        if data.get('attending') is False:
            data['has_companion'] = False
        return data