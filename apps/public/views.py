# -*- coding: utf-8 -*-
from __future__ import absolute_import
from django import template
from django.conf import settings
from django.contrib import comments
from django.contrib.auth.decorators import login_required
from django.contrib.comments.views.utils import next_redirect
from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.comments.views.moderation import perform_delete


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
        return render_to_response(
            'comments/delete.html',
            {'comment': comment, "next": next},
            template.RequestContext(request)
        )


def no_registration(request):
    return render_to_response(
        "public/no_registration.html",
        {},
        template.RequestContext(request)
    )
