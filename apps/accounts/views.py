from django import http
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.views.generic.edit import FormView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
import account.views
from .forms import ZythonLoginForm, ZythonSettingForm, ZythonSignupForm


class LoginView(account.views.LoginView):
    form_class = ZythonLoginForm


class SettingsView(LoginRequiredMixin, FormView):
    model = User
    form_class = ZythonSettingForm
    template_name = "account/settings.html"
    success_url = "."

    def get_form_kwargs(self):
        kwargs = super(SettingsView, self).get_form_kwargs()
        kwargs["instance"] = self.request.user
        return kwargs

    def form_valid(self, form):
        user = form.save()
        update_session_auth_hash(self.request, user)
        messages.add_message(self.request, messages.SUCCESS, _("Changes saved"))
        return http.HttpResponseRedirect(".")


class SignupView(account.views.SignupView):
    form_class = ZythonSignupForm


def new_socialuser(request):
    messages.add_message(request, messages.SUCCESS, _(u"Welcome to you ! Please review your account settings before using Zython"))
    return http.HttpResponseRedirect("/account/settings/")
