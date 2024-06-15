from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render
from django.views import View

from wfd.controllers.can_admin import can_admin
from wfd.controllers.context_creator import create_context
from wfd.models import Attendant, Workshop


class Participants(UserPassesTestMixin, View):

    def test_func(self):
        return can_admin(self.request.user)

    def get(self, request):
        attendants = Attendant.objects.all().order_by('-workshop__date')
        attendance = {}
        for attendant in attendants:
            workshop_name = f"{attendant.workshop}"
            if workshop_name in attendance:
                attendance[workshop_name].append(attendant.sfuid)
            else:
                attendance[workshop_name] = [attendant.sfuid]
        return render(
            request, 'participants.html',
            create_context(request, "participants", workshops=Workshop.objects.all(),
                           attendance=attendance)
        )
