# -*- coding: utf-8 -*-
from __future__ import absolute_import
from django import template
from django.conf import settings
import django_comments as comments
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django_comments.views.utils import next_redirect
from django_comments.views.moderation import perform_delete


@login_required
def comment_delete(request, comment_id, next=None):
    """
    Override the django.contrib.comments.views.moderation.delete()
    No need to have the comments.can_moderate permission
    """
    comment = get_object_or_404(comments.get_model(), pk=comment_id, site__pk=settings.SITE_ID)

    # Delete on POST
    if request.method == 'POST':
        # Flag the comment as deleted instead of actually deleting it.
        perform_delete(request, comment)
        return next_redirect(request, next)

    # Render a form on GET
    else:
        return render(
            request,
            'comments/delete.html',
            {'comment': comment, "next": next}
        )


def no_registration(request):
    return render(
        request,
        "public/no_registration.html"
    )
