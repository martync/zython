from django import http
from units import settings as app_settings


class UnitViewFormMixin(object):
    def get_form_kwargs(self):
        kwargs = super(UnitViewFormMixin, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


def set_unit(request, unit, locale):
	next = request.META.get("HTTP_REFERER", request.GET.get("next", request.POST.get("next", "/")))
	prefix = getattr(app_settings, 'CONTEXT_PREFIX', 'unit_')
	request.session["%s%s" % (prefix, unit)] = locale
	return http.HttpResponseRedirect(next)