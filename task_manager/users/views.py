from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import (
    LoginView,
    LogoutView
)
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.utils.translation import gettext_lazy as _

from task_manager.users.forms import (
    CustomUserCreateForm,
    LoginUserForm,
    CustomUserUpdateForm,
)


class UsersListView(ListView):
    model = User
    template_name = 'users/users.html'
    context_object_name = 'users'
    ordering = ['pk']


class UserCreateView(SuccessMessageMixin,
                     CreateView):
    model = User
    form_class = CustomUserCreateForm
    template_name = 'users/user_create.html'
    success_url = reverse_lazy('login')
    success_message = _('User successfully added')


class UserUpdateView(LoginRequiredMixin,
                     SuccessMessageMixin,
                     UpdateView):
    model = User
    form_class = CustomUserUpdateForm
    template_name = 'users/user_update.html'
    success_url = reverse_lazy('users_list')
    success_message = _('User successfully updated')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj != self.request.user:
            messages.error(self.request,
                           _('You do not have permission'
                             ' to edit another user'))
            return redirect('users_list')
        return super().dispatch(request, *args, **kwargs)


class UserDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = User
    template_name = 'users/user_delete.html'
    success_url = reverse_lazy('users_list')
    success_message = _('User successfully deleted')

    def dispatch(self, request, *args, **kwargs):
        try:
            obj = self.get_object()
            if obj != self.request.user:
                messages.error(self.request,
                               _('You do not have permission'
                                 ' to delete another user'))
                return redirect('users_list')
            return super().dispatch(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, _('Unable to delete user'))
            return redirect(self.success_url)


class UserLoginView(SuccessMessageMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    success_url = reverse_lazy('index')
    success_message = _('You are logged in')


class UserLogoutView(LogoutView):
    next_page = 'index'

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, _('You are logged out'))
        return super().dispatch(request, *args, **kwargs)
