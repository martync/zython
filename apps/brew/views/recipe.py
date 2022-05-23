import io
import zipfile

from django import http
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, CreateView, DetailView, DeleteView
from django.views.generic.edit import FormView, UpdateView
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin

from units.views import UnitViewFormMixin
from guardian.shortcuts import get_users_with_perms, assign, get_perms_for_model, remove_perm
from fm.views import JSONResponseMixin

from ..decorators import recipe_author
from .base import RecipeAuthorMixin, RecipeSlugUrlMixin, RecipeViewableMixin, SLUG_MODELROOT, SLUG_MODELFORM
from ..models import Recipe
from ..forms import RecipeSearchForm, RecipeImportForm, RecipeForm, EfficiencyCalculatorForm
from ..helpers import import_beer_xml

__all__ = (
    "RecipeListView", "UserRecipeListView", "UserListView", "RecipeCreateView", "RecipeImportView",
    "RecipeDetailView", "RecipeDeleteView", "RecipeUpdateView", "RecipeCloneView", "RecipeEfficiencyCalculatorView",
    "RecipeExportView", "set_user_perm"
)


class RecipeListView(ListView):
    user = None

    def search_form(self, qs):
        if self.kwargs.get("username"):
            # Display User page
            user = get_object_or_404(User, username=self.kwargs.get("username"))
            self.user = user
            qs = qs.filter(user=user)
        else:
            if self.request.GET:
                search_form = RecipeSearchForm(self.request.GET)
                if search_form.is_valid():
                    qs = search_form.search(qs)
            else:
                search_form = RecipeSearchForm()
            self.search_form = search_form
        return qs

    def get_queryset(self):
        qs = Recipe.objects.for_user(self.request.user).select_related('user', 'style')
        return self.search_form(qs)

    def get_context_data(self, **kwargs):
        context = super(RecipeListView, self).get_context_data(**kwargs)
        context['user_recipe'] = self.user
        if self.user is None:
            context['search_form'] = getattr(self, 'search_form')
        return context


class UserRecipeListView(RecipeListView):
    def get_queryset(self):
        qs = Recipe.objects.filter(user=self.request.user).select_related('user', 'style')
        return self.search_form(qs)


class UserListView(ListView):
    model = User
    template_name = "brew/user_list.html"

    def get_queryset(self):
        qs = super(UserListView, self).get_queryset()
        return qs.filter(recipe__private=False).distinct().order_by("-date_joined")


class RecipeCreateView(LoginRequiredMixin, UnitViewFormMixin, CreateView):
    form_class = RecipeForm
    model = Recipe

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save()
        return http.HttpResponseRedirect(self.object.get_absolute_url())

    def get_initial(self):
        """Get the previous data used."""
        initial = super(CreateView, self).get_initial()
        recipes = self.request.user.recipe_set.all().order_by('-created')
        if recipes.count() > 0:
            recipe = recipes[0]
            initial['boiler_tun_deadspace'] = recipe.boiler_tun_deadspace
            initial['mash_tun_deadspace'] = recipe.mash_tun_deadspace
            initial['evaporation_rate'] = recipe.evaporation_rate
        return initial


class RecipeExportView(UserListView):
    template_name = "brew/recipe_export.html"

    def get(self, request, *args, **kwargs):
        if request.GET.get("format") == "pdf":
            return self.download_pdf(request)
        return super(RecipeExportView, self).get(request, *args, **kwargs)

    def download_pdf(self, request):
        user = request.user
        b = io.BytesIO()
        zf = zipfile.ZipFile(b, mode='w')

        qs = Recipe.objects.filter(user=user).select_related('user', 'style')
        for q in qs:
            recipe_txt = q.get_as_text(extra_context={"request": request})
            zf.writestr('{}.txt'.format(q.slug_url), recipe_txt)

        zf.close()
        response = http.HttpResponse(b.getbuffer())
        response['Content-Type'] = 'application/x-zip-compressed'
        response['Content-Disposition'] = 'attachment; filename=zython-recipes-{}.zip'.format(user.username)
        return response



class RecipeImportView(LoginRequiredMixin, FormView):
    form_class = RecipeImportForm
    template_name = "brew/recipe_import_form.html"

    def post(self, *args, **kwargs):
        xml_data = self.request.FILES.get('beer_file').read()
        import_beer_xml(xml_data, self.request.user)
        return http.HttpResponseRedirect(reverse(
            'brew_recipe_user',
            args=[self.request.user.username]
        ))


class RecipeDetailView(RecipeSlugUrlMixin, RecipeViewableMixin, DetailView):
    model = Recipe
    pk_url_kwarg = 'pk'
    page = "detail"

    def dispatch(self, *args, **kwargs):
        response = super(RecipeDetailView, self).dispatch(*args, **kwargs)
        if "permissions" in self.template_name_suffix and self.request.user != self.object.user:
            return http.HttpResponseRedirect(self.object.get_absolute_url())
        return response

    def render_to_response(self, context, **kwargs):
        if self.template_name_suffix == "_text":
            return http.HttpResponse(
                self.object.get_as_text(extra_context={"request": self.request}),
                content_type="text/plain; charset=utf-8"
            )
        return super(RecipeDetailView, self).render_to_response(
            context, **kwargs
        )

    def get_template_names(self):
        if self.template_name_suffix == "_text":
            return "brew/recipe_detail.txt"
        return super(RecipeDetailView, self).get_template_names()

    def get_context_data(self, **kwargs):
        context = super(RecipeDetailView, self).get_context_data(**kwargs)
        if self.request.user.is_active:
            for key, model in SLUG_MODELROOT.items():
                context['%s_list' % key] = model.objects.all()
                context['%s_form' % key] = SLUG_MODELFORM[key](request=self.request)
        self.template_name_suffix = "_%s" % self.page
        can_edit = self.request.user == self.object.user or self.request.user.has_perm('change_recipe', self.object)
        if self.page == "print":
            can_edit = False
        elif self.page == "permissions":
            context['user_perms'] = get_users_with_perms(self.object)
            context['object_perms'] = get_perms_for_model(self.object)

        context.update({
            'page': self.page,
            'calculator_form': EfficiencyCalculatorForm(self.request, initial={
                "collected_volume": self.object.batch_size,
                "measured_gravity": self.object.get_original_gravity()
            }),
            'can_edit': can_edit
        })
        return context


class RecipeDeleteView(RecipeSlugUrlMixin, RecipeAuthorMixin, DeleteView):
    success_url = "/"

    def get_context_data(self, **kwargs):
        context = super(RecipeDeleteView, self).get_context_data(**kwargs)
        context['page'] = "delete"
        context['can_edit'] = self.request.user == self.object.user
        return context


class RecipeUpdateView(RecipeSlugUrlMixin, RecipeAuthorMixin, UnitViewFormMixin, UpdateView):
    form_class = RecipeForm


class RecipeCloneView(RecipeSlugUrlMixin, LoginRequiredMixin, RecipeViewableMixin, JSONResponseMixin, DetailView):
    template_name = "brew/recipe_clone.html"

    def post(self, *args, **kwargs):
        self.object = self.get_object()
        new_recipe = self.object.clone_to_user(self.request.user)
        url = new_recipe.get_absolute_url()
        if self.request.is_ajax():
            return self.render_json_response({'status': 'redirect', 'message': "<script>window.location='%s'</script>" % url})
        return http.HttpResponseRedirect(url)


class RecipeEfficiencyCalculatorView(UnitViewFormMixin, FormView):
    http_method_names = ['post', ]  # accept only POSTs
    form_class = EfficiencyCalculatorForm

    def form_invalid(self, form):
        # TODO : add error output
        return http.HttpResponse("error")

    def form_valid(self, form):
        recipe = get_object_or_404(Recipe, pk=self.kwargs["recipe_id"])
        sg = float(form.cleaned_data["measured_gravity"])
        vol = float(form.cleaned_data["collected_volume"])
        efficiency = recipe.compute_empirical_efficiency(vol, sg)
        return http.JsonResponse({"efficiency": efficiency})


@login_required
@recipe_author
def set_user_perm(request, recipe, recipe_id, slug):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    username = request.POST.get('username')
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        messages.error(request, _("User %s does not exist" % username))
    else:
        raw_perms = request.POST.get('perms')
        perms = raw_perms.split("|")
        init_perms = ['change_recipe', 'view_recipe']
        for perm in init_perms:
            remove_perm(perm, user, recipe)
        for perm in perms:
            if perm:
                assign(perm, user, recipe)
        if raw_perms:
            messages.success(request, _("Permissions added for user %s" % username))
        else:
            messages.success(request, _("Permissions removed for user %s" % username))
    return http.HttpResponseRedirect(reverse('brew_recipe_permissions', args=[recipe_id, recipe.slug_url]))
