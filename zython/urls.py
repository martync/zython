from django.conf.urls.static import static
from django.urls import re_path, include, path
from django.conf import settings
from django.contrib import admin
from django.views.generic import TemplateView
from brew.views.recipe import RecipeListView
import accounts.views
from public.views import comment_delete

admin.autodiscover()

urlpatterns = [

    re_path(r'^$',
        RecipeListView.as_view(),
        name='root_url'),

    re_path(r"^account/login/$",
        accounts.views.LoginView.as_view(),
        name="account_login"),

    re_path(r"^account/signup/$",
        accounts.views.SignupView.as_view(),
        name="account_signup"),

    re_path(r"^account/settings/$",
        accounts.views.SettingsView.as_view(),
        name="account_settings"),

    re_path(r"^account/new-social-auth-user/$",
        accounts.views.new_socialuser,
        name="account_new_socialuser"),

    re_path(r'^comment-delete/(\d+)/',
        comment_delete,
        name="comment-delete"),

    re_path(r'^how-it-works/',
        TemplateView.as_view(template_name="how.html"),
        name="how_it_works"),

    re_path(r'login/recipe/$',
        RecipeListView.as_view(),
        name="login_recipe"),

    re_path(r'^email_test/',
        TemplateView.as_view(template_name="base_email.html"),
        name="dfgfdg"),

    re_path(r"^account/", include("account.urls")),
    re_path(r'^recipe/', include('brew.urls')),
    re_path(r'^stocks/', include('stocks.urls')),
    re_path(r'^units/', include('units.urls')),
    re_path(r'^comments/', include('django_comments.urls')),
    re_path(r'^i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

