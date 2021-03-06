from django.conf.urls import url

from .urls import USER_URL_PREFIX, EDIT_URL_PREFIX
from . import views

# These need to be listed before the exercise URL routings.
urlpatterns = [
    url(USER_URL_PREFIX + r'enroll/$',
        views.Enroll.as_view(),
        name='enroll'),
    url(USER_URL_PREFIX + r'export-calendar/$',
        views.CalendarExport.as_view(),
        name='export-calendar'),
    url(USER_URL_PREFIX + r'groups/$',
        views.GroupsView.as_view(),
        name="groups"),
    url(USER_URL_PREFIX + r'groups/select/$',
        views.GroupSelect.as_view(),
        name="group-select"),
    url(EDIT_URL_PREFIX + r'participants/$',
        views.ParticipantsView.as_view(),
        name="participants"),
    # url(USER_URL_PREFIX + r'filter-categories/$',
    #     views.FilterCategories.as_view(),
    #     name='filter-categories'),
]
