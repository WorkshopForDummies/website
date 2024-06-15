from django.shortcuts import render
from django.views import View

from wfd.controllers.can_admin import can_admin
from wfd.controllers.context_creator import create_context
from wfd.models import Workshop, pstdatetime


class Workshops(View):

    def get(self, request):
        return render(
            request, 'workshops.html',
            create_context(
                request, 'workshops', workshops=Workshop.objects.all().order_by('-date'),
                workshop_types=True
            )
        )

    def post(self, request):
        if can_admin(request.user):
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


class WorkshopParticipantInstructions(View):

    def get(self, request, workshop_id):
        matching_workshop = Workshop.objects.all().filter(id=workshop_id).first()
        if matching_workshop:
            year = matching_workshop.date.year
            month = matching_workshop.date.month
            day = matching_workshop.date.day
            workshop_type = matching_workshop.workshop_type
            return render(
                request, f'workshop_instructions/{year}_{month}_{day}_{workshop_type}.html',
                {"workshop_id": workshop_id})
