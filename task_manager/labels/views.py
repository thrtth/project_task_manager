from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin

from task_manager.labels.forms import LabelForm
from task_manager.labels.models import Label


class LabelListView(LoginRequiredMixin, ListView):
    model = Label
    template_name = 'labels/labels.html'
    context_object_name = 'labels'
    ordering = ['id']


class LabelCreateView(LoginRequiredMixin,
                      SuccessMessageMixin,
                      CreateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/label_create.html'
    success_url = reverse_lazy('labels')
    success_message = _('Label successfully created')


class LabelUpdateView(LoginRequiredMixin,
                      SuccessMessageMixin,
                      UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/label_update.html'
    success_url = reverse_lazy('labels')
    success_message = _('Label successfully updated')


class LabelDeleteView(LoginRequiredMixin,
                      SuccessMessageMixin,
                      DeleteView):
    model = Label
    template_name = 'labels/label_delete.html'
    success_url = reverse_lazy('labels')
    success_message = _('Label successfully deleted')

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.label_tasks.exists():
            messages.error(request, _('Cannot delete the label'))
            return redirect(reverse('labels'))
        return super().post(request, *args, **kwargs)
