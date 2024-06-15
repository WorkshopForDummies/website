from django.contrib.auth.decorators import login_required
from django.urls import path, re_path

from wfd.controllers.participant_feedback_form_view import ShowFeedBackForms, ParticipantFeedBackFormView, ListFeedBackResponses
from wfd.controllers.admin_feedback_questions import CreateFeedBackQuestion, UpdateOrDeleteFeedBackQuestion
from wfd.controllers.index import IndexPage
from wfd.controllers.logins import LoginView, LogoutView
from wfd.controllers.participants import Participants
from wfd.controllers.sign_in import SignIn
from wfd.controllers.workshops import Workshops, WorkshopParticipantInstructions

urlpatterns = [
    path(r"", IndexPage.as_view(), name='index'),
    re_path(r"^signin/(?P<workshop_id>[0-9A-Aa-z\-]*)", login_required(SignIn.as_view()), name='sign_in'),
    re_path(r"^feedback_forms$", login_required(ShowFeedBackForms.as_view()), name="show_feedback_forms"),
    re_path(r"^feedback_forms/(?P<workshop_id>[0-9A-Aa-z\-]*)/question", login_required(CreateFeedBackQuestion.as_view()), name="feedback_form"),
    re_path(r"^feedback_forms/questions/(?P<question_id>[0-9]*)", login_required(UpdateOrDeleteFeedBackQuestion.as_view()), name="feedback_form"),
    re_path(r"^feedback_form/(?P<workshop_id>[0-9A-Aa-z\-]*)$", login_required(ParticipantFeedBackFormView.as_view()), name="feedback_form"),
    re_path(f"^feedback_responses", login_required(ListFeedBackResponses.as_view()), name='feedback_responses'),
    re_path(r'^participants', login_required(Participants.as_view()), name='participants'),
    re_path(r"^workshop_instructions/(?P<workshop_id>[0-9A-Aa-z\-]*)$", login_required(WorkshopParticipantInstructions.as_view()), name="workshop_instructions"),
    re_path(r'^workshops', login_required(Workshops.as_view()), name='workshops'),
    re_path(r"^login", LoginView.as_view(), name='login'),
    re_path(r"^logout", LogoutView.as_view(), name='logout'),
]