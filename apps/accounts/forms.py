from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from brew.utils.forms import BS3FormMixin
from account.forms import LoginUsernameForm, SignupForm


class ZythonSignupForm(BS3FormMixin, SignupForm):
    pass


class ZythonLoginForm(BS3FormMixin, LoginUsernameForm):
    pass


class ZythonSettingForm(BS3FormMixin, UserChangeForm):
    new_password1 = forms.CharField(label=_("New password"), widget=forms.PasswordInput, help_text=_(u"If you don't want to change your password, let those fields blank"), required=False)
    new_password2 = forms.CharField(label=_("New password confirmation"), widget=forms.PasswordInput, required=False)

    def __init__(self, *args, **kwargs):
        super(ZythonSettingForm, self).__init__(*args, **kwargs)
        self.user = self.instance
        del self.fields['password']
        self.fields["username"].help_text = u'%s%s' % (_(u"This is what the world will see about you. Choosing a good username is usually a good thing."), self.fields["username"].help_text)
        self.fields["email"].required = True

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 or password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        return password2

    def save(self, *args, **kwargs):
        user = super(ZythonSettingForm, self).save(*args, **kwargs)
        password1 = self.cleaned_data.get('new_password1')
        if password1:
            user.set_password(password1)
            user.save()
        return user

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
