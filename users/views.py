from django.views.generic import UpdateView, CreateView
from users.models import User
from django.urls import reverse_lazy
from users.forms import UserForm, UserRegisterForm


class ProfileUpdateView(UpdateView):

    model = User
    form_class = UserForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class RegisterView(CreateView):

    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('catalog:index')
