from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from wfd.controllers.context_creator import create_context
from wfd.models import Workshop, pstdatetime


class Workshops(View):

    def get(self, request):
        if request.user.is_anonymous:
            return HttpResponseRedirect(f"/login?next={request.path}")
        return render(
            request, 'workshops.html',
            create_context(
                request, 'workshops', workshops=Workshop.objects.all().order_by('-date'),
                workshop_types=True
            )
        )

    def post(self, request):
        if request.user.is_anonymous:
            return HttpResponseRedirect(f"/login?next={request.path}")
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
        elif action == 'Flip Status':
            matching_workshop = Workshop.objects.all().filter(id=request.POST.get("id")).first()
            if matching_workshop:
                matching_workshop.in_progress = not matching_workshop.in_progress
                matching_workshop.save()
        return self.get(request)

