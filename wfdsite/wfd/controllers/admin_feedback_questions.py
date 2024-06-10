from django.http import HttpResponseRedirect
from django.views import View
from wfd.models import FeedBackQuestion as FeedBackQuestionModel


class CreateFeedBackQuestion(View):

    def post(self, request, workshop_id):
        if request.user.is_anonymous:
            return HttpResponseRedirect(f"/login?next={request.path}")
        FeedBackQuestionModel(question=request.POST.get("question"),workshop_id=workshop_id).save()
        return HttpResponseRedirect("/feedback_forms")


class UpdateOrDeleteFeedBackQuestion(View):

    def post(self, request, question_id):
        if request.user.is_anonymous:
            return HttpResponseRedirect(f"/login?next={request.path}")
        action = request.POST.get("action")
        question = FeedBackQuestionModel.objects.all().filter(id=question_id).first()
        if question is not None:
            if action == 'Update':
                question.question = request.POST.get("question")
                question.save()
            elif action == 'Delete':
                question.delete()
        return HttpResponseRedirect("/feedback_forms")
