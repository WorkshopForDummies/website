from django.shortcuts import render
from django.views import View

from wfd.models import Attendant, Workshop


class Participants(View):

    def get(self, request):
        return render(
            request, 'participants.html',
            {
                "attendants": Attendant.objects.all().order_by('-workshop__date'),
                "workshops": Workshop.objects.all(),
                "sfuid": request.user.username,
                "page": "participants"
            }
        )
