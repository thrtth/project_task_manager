from django import forms
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Label


class LabelForm(forms.ModelForm):

    class Meta:
        model = Label
        fields = ['name']
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control',
                       'placeholder': _('Name')}),
        }
