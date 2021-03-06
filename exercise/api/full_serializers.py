from rest_framework import serializers
from rest_framework_extensions.fields import NestedHyperlinkedIdentityField

from lib.api.serializers import (
    AlwaysListSerializer,
    CompositeListSerializer,
    AplusSerializerMeta,
    AplusModelSerializerBase,
)
from course.api.serializers import CourseBriefSerializer
from userprofile.api.serializers import UserBriefSerializer, UserListField

from ..models import Submission
from .serializers import ExerciseBriefSerializer, SubmissionBriefSerializer


__all__ = [
    'ExerciseSerializer',
    'ExerciseGraderSerializer',
    'SubmitterStatsSerializer',
    'UserListFieldWithStatsLink',
    'SubmissionSerializer',
    'SubmissionGraderSerializer',
]


class ExerciseSerializer(ExerciseBriefSerializer):
    course = CourseBriefSerializer(source='course_instance')
    post_url = serializers.SerializerMethodField()
    exercise_info = serializers.JSONField()
    submissions = NestedHyperlinkedIdentityField(
        view_name='api:exercise-submissions-list',
        lookup_map='exercise.api.views.ExerciseViewSet',
    )
    my_submissions = NestedHyperlinkedIdentityField(
        view_name='api:exercise-submissions-detail',
        lookup_map={
            'exercise_id': 'id',
            'user_id': lambda o=None: 'me',
        },
    )
    my_stats = NestedHyperlinkedIdentityField(
        view_name='api:exervise-submitter_stats-detail',
        lookup_map={
            'exercise_id': 'id',
            'user_id': lambda o=None: 'me',
        },
    )

    def get_post_url(self, obj):
        # FIXME: obj should implement .get_post_url() and that should be used here
        if obj.is_submittable:
            request = self.context['request']
            url = obj.get_url("exercise")
            return request.build_absolute_uri(url)
        return None

    class Meta(ExerciseBriefSerializer.Meta):
        fields = (
            'name',
            'course',
            'is_submittable',
            'post_url',
            'max_points',
            'max_submissions',
            'exercise_info',
            'submissions',
            'my_submissions',
            'my_stats',
        )


class ExerciseGraderSerializer(AplusModelSerializerBase):
    url = NestedHyperlinkedIdentityField(
        view_name='api:exercise-grader',
        lookup_map='exercise.api.views.ExerciseViewSet',
    )
    exercise = ExerciseBriefSerializer(source='*')

    class Meta(AplusSerializerMeta):
        model = Submission
        fields = (
            'url',
            'exercise',
        )


class SubmitterStatsSerializer(serializers.Serializer):
    url = NestedHyperlinkedIdentityField(
        view_name='api:exervise-submitter_stats-detail',
        lookup_map={
            'exercise_id': 'exercise_id',
            'user_id': 'user.user_id',
        },
    )
    exercise = NestedHyperlinkedIdentityField(
        view_name='api:exercise-detail',
        lookup_map={ 'exercise_id': 'exercise_id' },
    )
    user = UserBriefSerializer()
    submission_count = serializers.IntegerField()
    best_submission = SubmissionBriefSerializer()
    grade = serializers.IntegerField()

    class Meta(AplusSerializerMeta):
        fields = (
            'url',
            'exercise',
            'user',
            'submission_count',
            'best_submission',
            'grade',
        )


class UserListFieldWithStatsLink(AlwaysListSerializer, UserBriefSerializer):
    exercise_stats = NestedHyperlinkedIdentityField(
        view_name='api:exervise-submitter_stats-detail',
        lookup_map={
            'exercise_id': 'exercise_id',
            'user_id': 'user_id',
        },
    )

    class Meta(UserBriefSerializer.Meta):
        list_serializer_class = CompositeListSerializer.with_extra({
            'exercise_id': 'exercise_id',
        })
        fields = (
            'exercise_stats',
        )


class SubmissionSerializer(SubmissionBriefSerializer):
    exercise = ExerciseBriefSerializer()
    submitters = UserListFieldWithStatsLink()

    class Meta(SubmissionBriefSerializer.Meta):
        fields = (
            'html_url',
            'exercise',
            'submitters',
            'status',
            'grade',
            'grading_time',
        )


class SubmissionInGraderSerializer(SubmissionBriefSerializer):
    class Meta(SubmissionBriefSerializer.Meta):
        fields = (
            'html_url',
        )


class SubmissionGraderSerializer(AplusModelSerializerBase):
    url = NestedHyperlinkedIdentityField(
        view_name='api:submission-grader',
        lookup_map='exercise.api.views.SubmissionViewSet',
    )
    submission = SubmissionInGraderSerializer(source='*')
    exercise = ExerciseBriefSerializer()

    class Meta(AplusSerializerMeta):
        model = Submission
        fields = (
            'url',
            'submission',
            'exercise',
            'grading_data',
            'is_graded',
        )


class SubmissionDataSerializer(SubmissionSerializer):
    submitters = UserListField()
    submission_data = serializers.JSONField()
    grading_data = serializers.JSONField()

    class Meta(SubmissionSerializer.Meta):
        fields = (
            'late_penalty_applied',
            'submission_data',
            'grading_data',
        )
