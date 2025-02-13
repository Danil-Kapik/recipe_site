from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm


class RegisterView(FormView):
    template_name = 'myauth/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('recipes:index')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
