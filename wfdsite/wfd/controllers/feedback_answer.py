from django.http import HttpResponseRedirect
from django.views import View
from wfd.models import FeedbackAnswer as FeedbackAnswerModel


class CreateFeedBackAnswer(View):

    def post(self, request, workshop_id):
        FeedbackAnswerModel(
            question=request.POST.get("question"),
            workshop_id=int(workshop_id)).save()
        return HttpResponseRedirect("/feedback_forms")


class UpdateOrDeleteFeedBackAnswer(View):

    def post(self, request, question_id):
        action = request.POST.get("action")
        question = FeedbackAnswerModel.objects.all().filter(id=question_id).first()
        if question is not None:
            if action == 'Update':
                question.question = request.POST.get("question")
                question.save()
            elif action == 'Delete':
                question.delete()
        return HttpResponseRedirect("/feedback_forms")
