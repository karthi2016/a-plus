from django.conf import settings
from django.conf.urls import url, include
from rest_framework_extensions.routers import ExtendedDefaultRouter

import userprofile.api.views, \
       course.api.views
from exercise.api.views import *
import exercise.api.views


api = ExtendedDefaultRouter()

api.register(r'users',
             userprofile.api.views.UserViewSet,
             base_name='user')

with api.register(r'exercises',
                    exercise.api.views.ExerciseViewSet,
                    base_name='exercise') as exercises:
    exercises.register(r'submissions',
                        exercise.api.views.ExerciseSubmissionsViewSet,
                        base_name='exercise-submissions')

with api.register(r'courses',
                  course.api.views.CourseViewSet,
                  base_name='course') as courses:
    courses.register(r'exercises',
                     course.api.views.CourseExercisesViewSet,
                     base_name='course-exercises')
    courses.register(r'students',
                     course.api.views.CourseStudentsViewSet,
                     base_name='course-students')
    courses.register(r'points',
                     course.api.views.CoursePointsViewSet,
                     base_name='course-points')

urlpatterns = [
    url(r'^', include(api.urls, namespace='api')),

    url(r'^me', userprofile.api.views.MeDetail.as_view()),

    # For login/logout etc. pages in Django REST Framework
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]

if settings.DEBUG:
    print(" API URLS:")
    for url in api.urls:
        print("  - %r" % (url,))