from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from wfd.controllers.context_creator import create_context
from wfd.models import Workshop, FeedBackQuestion, FeedbackAnswer, Attendant

from querystring_parser import parser


class ShowFeedBackForms(View):

    def get(self, request):
        if request.user.is_anonymous:
            return HttpResponseRedirect(f"/login?next={request.path}")
        return render(
            request, 'feedback_forms.html',
            create_context(request, "feedback_forms", workshops=Workshop.objects.all().order_by('-date'))
        )


class ParticipantFeedBackFormView(View):

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
                    "question_id": question.id,
                    "answer": answer
                })

        return render(
            request, 'feedback_form.html',
            create_context(request, "feedback_form", question_and_answers=question_and_answers)
        )

    def post(self, request, workshop_id):
        if request.user.is_anonymous:
            return HttpResponseRedirect(f"/login?next={request.path}")
        post_dict = parser.parse(request.POST.urlencode())
        user_answers = {
            answer.question.id: answer
            for answer in FeedbackAnswer.objects.all().filter(attendant__sfuid=request.user.username)
        }
        attendant = Attendant.objects.all().filter(sfuid=request.user.username).first()
        workshop = None
        for question_id, answer in post_dict['answers'].items():
            if workshop is None:
                workshop = Workshop.objects.all().filter(
                    feedbackquestion__id=question_id
                ).first()
                print(workshop)
            answer_obj = user_answers.get(
                question_id,
                FeedbackAnswer(
                    attendant=attendant,
                    question_id=question_id
                )
            )
            answer_obj.answer = answer
            answer_obj.save()
        return self.get(request, workshop_id)


class ListFeedBackResponses(View):
    def get(self, request):
        if request.user.is_anonymous:
            return HttpResponseRedirect(f"/login?next={request.path}")
        feedback_form_questions = FeedBackQuestion.objects.all().order_by('workshop')
        questions = {}
        for feedback_form_question in feedback_form_questions:
            workshop_name = f"{feedback_form_question.workshop}"
            relevant_answers = FeedbackAnswer.objects.all().filter(
                question=feedback_form_question
            )
            relevant_answers = [
                relevant_answer for relevant_answer in relevant_answers
                if len(relevant_answer.answer) > 0
            ]
            if workshop_name not in questions:
                questions[workshop_name] = [
                    {
                        "question": feedback_form_question.question,
                        "answers": relevant_answers
                    }
                ]
            else:
                questions[workshop_name].append({
                    "question": feedback_form_question.question,
                    "answers": relevant_answers
                })

        return render(
            request, 'feedback_forms_responses.html',
            create_context(request, "feedback_responses", feedback_responses=questions)
        )
