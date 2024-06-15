from django.http import HttpResponseRedirect
from django.views import View

from wfd.controllers.can_admin import can_admin
from wfd.models import FeedBackQuestion as FeedBackQuestionModel


class CreateFeedBackQuestion(View):

    def test_func(self):
        return can_admin(self.request.user)

    def post(self, request, workshop_id):
        FeedBackQuestionModel(question=request.POST.get("question"),workshop_id=workshop_id).save()
        return HttpResponseRedirect("/feedback_forms")


class UpdateOrDeleteFeedBackQuestion(View):

    def test_func(self):
        return can_admin(self.request.user)

    def post(self, request, question_id):
        action = request.POST.get("action")
        question = FeedBackQuestionModel.objects.all().filter(id=question_id).first()
        if question is not None:
            if action == 'Update':
                question.question = request.POST.get("question")
                question.save()
            elif action == 'Delete':
                question.delete()
        return HttpResponseRedirect("/feedback_forms")
