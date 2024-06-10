from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from wfd.controllers.context_creator import create_context
from wfd.models import Workshop


class SignInLinks(View):

    def get(self, request):
        if request.user.is_anonymous:
            return HttpResponseRedirect(f"/login?next={request.path}")
        signin_links = {
            f"/signin/{workshop.id}": f"{workshop}"
            for workshop in Workshop.objects.all()
        }
        return render(
            request, 'signin_links.html',
            create_context(request, "sign_in_links", signin_links=signin_links)
        )
