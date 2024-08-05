from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from task_manager.statuses.models import Status
from task_manager.tasks.models import Task


class TaskForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': _('Name')})
    )
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={'class': 'form-control', 'placeholder': _('Description')}),
        required=False
    )
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        widget=forms.Select(
            attrs={'class': 'form-select', 'placeholder': _('Status')})
    )
    executor = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(
            attrs={'class': 'form-select', 'placeholder': _('Executor')}),
        required=False
    )

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        (self.fields['executor'].
         label_from_instance) = lambda obj: f'{obj.first_name} {obj.last_name}'
