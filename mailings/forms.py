from django import forms

from mailings.models import Mailing


class MailingCreateForm(forms.ModelForm):
    """Форма создания рассылки"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            self.fields['start_time'].required = True
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Mailing
        exclude = ('user', 'send_datetime', 'next_attempt')
        widgets = {
            'start_time': forms.DateInput(attrs=dict(type='datetime-local'))
        }


class MailingSettingsUpdateForm(forms.ModelForm):
    """Форма обновления рассылки"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Mailing
        exclude = ('subject', 'body', 'user', 'next_attempt')


class MailingSettingsManagerUpdateForm(MailingSettingsUpdateForm):
    """Форма оновления настроек рассылки для менеджера"""

    subject = forms.CharField(disabled=True, label="Тема")
    body = forms.CharField(disabled=True, label="Содержание рассылки")
    start_time = forms.DateTimeField(disabled=True, label='Дата начала рассылки:')

    class Meta:
        model = Mailing
        exclude = ('user', 'customers', 'interval',  'next_attempt')


