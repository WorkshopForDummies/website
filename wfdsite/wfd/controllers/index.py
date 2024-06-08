from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View


class IndexPage(View):

    def get(self, request):
        if request.user.is_anonymous:
            return HttpResponseRedirect("/login")
        return render(
            request, 'index.html',
            {
                "sfuid" : request.user.username,
                "page": "home"
            }
        )