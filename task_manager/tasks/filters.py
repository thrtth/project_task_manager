import django_filters
from django.contrib.auth.models import User
from django import forms

from task_manager.statuses.models import Status
from task_manager.tasks.forms import TaskFilterForm
from task_manager.tasks.models import Task
from task_manager.labels.models import Label


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(),
        widget=forms.Select(
            attrs={'class': 'form-select'}))
    executor = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        widget=forms.Select(
            attrs={'class': 'form-select'}))
    labels = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(),
        widget=forms.Select(
            attrs={'class': 'form-select'}))

    self_tasks = django_filters.BooleanFilter(
        method='get_my_tasks',
        widget=forms.CheckboxInput(
            attrs={'class': 'form-check-input'}))

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels', 'self_tasks']
        form = TaskFilterForm

    def get_my_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset
