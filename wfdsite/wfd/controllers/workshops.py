from django.shortcuts import render
from django.views import View

from wfd.models import Workshop, WORKSHOP_TYPES, pstdatetime


class Workshops(View):

    def get(self, request):
        return render(
            request, 'workshops.html',
            {
                "sfuid": request.user.username,
                "workshops": Workshop.objects.all().order_by('-date'),
                "workshop_types": WORKSHOP_TYPES,
                "page": "workshops"
            }
        )

    def post(self, request):
        action = request.POST.get("action")
        if action == 'Create':
            date = pstdatetime.create_pst_time_from_timestamp(request.POST.get("date"))
            workshop_type = request.POST.get("type")
            workshop_does_not_exist = Workshop.objects.all().filter(
                workshop_type=workshop_type,
                date=date
            ).first() is None
            if workshop_does_not_exist:
                Workshop(
                    workshop_type=workshop_type,
                    date=date
                ).save()
        elif action == 'Delete':
            matching_workshop = Workshop.objects.all().filter(id=request.POST.get("id")).first()
            if matching_workshop:
                matching_workshop.delete()
        return self.get(request)

