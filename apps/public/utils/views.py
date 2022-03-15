

class FormViewWithRequestMixin(object):
    "Adding request to form kwargs"

    def get_form_kwargs(self):
        kwargs = super(FormViewWithRequestMixin, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs
