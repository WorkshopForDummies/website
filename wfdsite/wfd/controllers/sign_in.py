from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from wfd.models import Attendant


class SignIn(View):
    def get(self, request, workshop_id):
        if request.user.is_anonymous:
            return HttpResponseRedirect(f"/login?next={request.path}")
        attendant = Attendant.objects.all().filter(
            sfuid=request.user.username, workshop__id=workshop_id).first()
        if attendant is None:
            Attendant(sfuid=request.user.username,workshop_id=workshop_id).save()
        return render(request, 'signed_in.html', {
            "sfuid": request.user.username,
            "page": "sign_in"
        })