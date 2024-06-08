from django.urls import path, re_path

from wfd.controllers.feedback_form import FeedBackForms, FeedBackForm, CreateFeedBackForm
from wfd.controllers.feedback_question import CreateFeedBackQuestion, UpdateOrDeleteFeedBackQuestion
from wfd.controllers.index import IndexPage
from wfd.controllers.logins import LoginView, LogoutView
from wfd.controllers.participants import Participants
from wfd.controllers.sign_in import SignIn
from wfd.controllers.workshops import Workshops

urlpatterns = [
    path(r"", IndexPage.as_view(), name='index'),
    re_path(r"^signin/(?P<workshop_id>[0-9A-Aa-z\-]*)", SignIn.as_view(), name='sign_in'),
    re_path(r"^feedback_forms$", FeedBackForms.as_view(), name="feedback_form"),
    re_path(r"^feedback_forms/(?P<workshop_id>[0-9A-Aa-z\-]*)/question", CreateFeedBackQuestion.as_view(), name="feedback_form"),
    re_path(r"^feedback_forms/questions/(?P<question_id>[0-9]*)", UpdateOrDeleteFeedBackQuestion.as_view(), name="feedback_form"),
    re_path(r"^feedback_form/(?P<workshop_id>[0-9A-Aa-z\-]*)$", FeedBackForm.as_view(), name="feedback_form"),
    re_path(r"^feedback_form/answers", CreateFeedBackForm.as_view(), name="feedback_form"),
    re_path(r'^participants', Participants.as_view(), name='participants'),
    re_path(r'^workshops', Workshops.as_view(), name='workshops'),
    re_path(r"^login", LoginView.as_view(), name='login'),
    re_path(r"^logout", LogoutView.as_view(), name='logout'),
]