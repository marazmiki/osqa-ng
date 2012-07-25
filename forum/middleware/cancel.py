# coding: utf-8

from django.shortcuts import redirect
from django.contrib import messages
from forum.forms import get_next_url


class CancelActionMiddleware(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if 'cancel' not in request.REQUEST:
            return

        message = getattr(view_func, 'CANCEL_MESSAGE', None) or 'action canceled'
        messages.success(request, message)

        return redirect(get_next_url(request))
