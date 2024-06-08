from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from wfd.models import Workshop, FeedBackQuestion, FeedbackAnswer, Attendant

from querystring_parser import parser
class FeedBackForms(View):

    def get(self, request):
        return render(
            request, 'feedback_forms.html',
            {
                "sfuid": request.user.username,
                "workshops": Workshop.objects.all().order_by('-date'),
                "page": "feedback_forms"
            }
        )


class FeedBackForm(View):

    def get(self, request, workshop_id):
        if request.user.is_anonymous:
            return HttpResponseRedirect(f"/login?next={request.path}")
        user_attended_workshop = Attendant.objects.all().filter(
            sfuid=request.user.username,
            workshop_id=workshop_id
        ).first()
        question_and_answers = []
        if user_attended_workshop:
            questions = FeedBackQuestion.objects.all().filter(workshop_id=workshop_id)
            current_answers = FeedbackAnswer.objects.all().filter(attendant__sfuid=request.user.username)

            for question in questions:
                answer_for_question = current_answers.filter(question_id=question.id).first()
                answer = answer_for_question.answer if answer_for_question else ""
                question_and_answers.append({
                    "question": question.question,
                    "question_id" : question.id,
                    "answer" : answer
                })
        return render(
            request, 'feedback_form.html',
            {
                "sfuid": request.user.username,
                "question_and_answers": question_and_answers,
                "page": "feedback_form"
            }
        )

class CreateFeedBackForm(View):

    def get(self, request):
        pass

    def post(self, request):
        post_dict = parser.parse(request.POST.urlencode())
        user_answers = {
            answer.question.id : answer
            for answer in FeedbackAnswer.objects.all().filter(attendant__sfuid=request.user.username)
        }
        attendant = Attendant.objects.all().filter(sfuid=request.user.username).first()
        workshop = None
        for question_id, answer in post_dict['answers'].items():
            if workshop is None:
                workshop = Workshop.objects.all().filter(
                    attendant__feedbackanswer__question_id=question_id
                ).first()
            answer_obj = user_answers.get(
                question_id,
                FeedbackAnswer(
                    attendant=attendant,
                    question_id=question_id
                )
            )
            answer_obj.answer = answer
            answer_obj.save()
        return HttpResponseRedirect(f"/feedback_form/{workshop.id}")
