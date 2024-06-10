from django.shortcuts import render


class CASAuthenticationMethod(Exception):
    def __init__(self, request, tab=None, error_message=None):
        context = {}
        if error_message is None:
            context['errors'] = ["Authentication method detected"]
        else:
            context['errors'] = [error_message]
        self.render = render(request, 'index.html', context)