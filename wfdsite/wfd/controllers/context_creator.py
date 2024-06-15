from wfd.controllers.can_admin import can_admin
from wfd.models import WORKSHOP_TYPES


def create_context(request, page, workshops=None, question_and_answers=None,
                   feedback_responses=None, attendance=None, workshop_types=False,
                   signin_links=None, workshop_name=None):
    context = {
        "sfuid": request.user.username,
        "page": page,
        'is_admin': can_admin(request.user),
    }
    if workshops:
        context['workshops'] = workshops
    if signin_links:
        context['signin_links'] = signin_links
    if workshop_name:
        context['workshop_name'] = workshop_name
    if question_and_answers:
        context['question_and_answers'] = question_and_answers
    if feedback_responses:
        context['feedback_responses'] = feedback_responses
    if attendance:
        context['attendance'] = attendance
    if workshop_types:
        context['workshop_types'] = WORKSHOP_TYPES
    return context
