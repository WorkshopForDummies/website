from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from wfd.controllers.context_creator import create_context


class IndexPage(View):

    def get(self, request):
        if request.user.is_anonymous:
            return HttpResponseRedirect(f"/login?next={request.path}")
        return render(request, 'index.html', create_context(request, "home"))
