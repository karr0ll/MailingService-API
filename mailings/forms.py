from django import forms

from mailings.models import Mailing


class MailingCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Mailing
        exclude = ('user',)
        widgets = {
            'start_time': forms.DateInput(attrs=dict(type='datetime-local'))
        }


class MailingSettingsUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Mailing
        exclude = ('subject', 'body', 'user')
