from account.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from .forms import NewUserForm


class MyProfile(LoginRequiredMixin, generic.UpdateView):
    queryset = User.objects.filter(is_active=True)
    fields = ('first_name', 'last_name',)
    success_url = reverse_lazy('home_page')

    def get_object(self, queryset=None):
        return self.request.user


class SignUpView(generic.CreateView):
    form_class = NewUserForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
