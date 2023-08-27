from django import forms

from customers.models import Customer


class CustomerCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Customer
        exclude = ['owner']
        # fields = '__all__'
