from django.shortcuts import render
from django.views import View

from wfd.controllers.can_admin import can_admin
from wfd.controllers.context_creator import create_context
from wfd.models import Attendant, Workshop


class SignIn(View):

    def test_func(self):
        return can_admin(self.request.user)

    def get(self, request, workshop_id):
        workshop = Workshop.objects.all().filter(id=workshop_id).first()
        if workshop is None:
            return render(
                request, 'workshop_doesnt_exist.html',
                create_context(request, "sign_in")
            )
        if not workshop.in_progress:
            return render(
                request, 'workshop_not_in_progress.html',
                create_context(request, 'sign_in', workshop_name=workshop)
            )
        attendant = Attendant.objects.all().filter(
            sfuid=request.user.username, workshop__id=workshop_id).first()
        if attendant is None:
            Attendant(sfuid=request.user.username, workshop_id=workshop_id).save()

        return render(request, 'signed_in.html', create_context(request, "sign_in"))
