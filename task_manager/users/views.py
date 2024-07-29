from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.translation import gettext as _

from task_manager.users.forms import CustomUserForm, LoginUserForm


class UsersListView(ListView):
    model = User
    template_name = 'users/users.html'
    context_object_name = 'users'
    ordering = ['pk']


class UserCreateView(CreateView):
    model = User
    form_class = CustomUserForm
    template_name = 'users/user_create.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _('User successfully added'))
        return response


class UserUpdateView(UpdateView):
    model = User
    form_class = CustomUserForm
    template_name = 'users/user_update.html'
    success_url = reverse_lazy('users_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _('User successfully updated'))
        return response

    def dispatch(self, request, *args, **kwargs):
        obj = get_object_or_404(User, pk=self.kwargs['pk'])
        if obj != self.request.user:
            messages.error(self.request, _('You do not have permission to edit another user'))
            return redirect('users_list')
        return super().dispatch(request, *args, **kwargs)


class UserDeleteView(DeleteView):
    model = User
    template_name = 'users/user_delete.html'
    success_url = reverse_lazy('users_list')

    def dispatch(self, request, *args, **kwargs):
        obj = get_object_or_404(User, pk=self.kwargs['pk'])
        if obj != self.request.user:
            messages.error(self.request, _('You do not have permission to delete another user'))
            return redirect('users_list')
        return super().dispatch(request, *args, **kwargs)


class UserLoginView(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _('You are logged in'))
        return response


class UserLogoutView(LogoutView):
    next_page = 'index'

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, _('You are logged out'))
        return super().dispatch(request, *args, **kwargs)
