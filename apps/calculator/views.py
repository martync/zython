from django.views.generic import TemplateView, FormView
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from calculator.forms import ABVForm


class CalculatorHomeView(TemplateView):
    template_name = "calculator/home.html"

    def get_context_data(self, *args, **kwargs):
        context = super(CalculatorHomeView, self).get_context_data(*args, **kwargs)
        context["form_urls"] = [
            ("abv", reverse("calculator_abv"), _("Average ABV %"))
        ]
        return context


class ABVView(FormView):
    template_name = "calculator/panel.html"
    form_class = ABVForm

    def form_valid(self, form, *args, **kwargs):
        context = self.get_context_data(form=form)
        context["results"] = form.get_results()
        return self.render_to_response(context)

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super(ABVView, self).get_form_kwargs(*args, **kwargs)
        form_kwargs["request"] = self.request
        return form_kwargs
