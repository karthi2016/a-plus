from rest_framework import serializers
from rest_framework.reverse import reverse
from rest_framework_extensions.fields import NestedHyperlinkedIdentityField
from lib.api.serializers import AplusModelSerializer, AlwaysListSerializer
from userprofile.api.serializers import UserBriefSerializer

from ..models import (
    CourseInstance,
    CourseModule,
    UserTag,
)


__all__ = [
    'CourseBriefSerializer',
    'CourseListField',
    'CourseUsertagBriefSerializer',
    'CourseSubmissionsBriefSerializer',
]


class CourseBriefSerializer(AplusModelSerializer):
    """
    BriefSerializer for course models
    """
    # course model has url var, so we need to redifen the type here
    url = NestedHyperlinkedIdentityField(
        view_name='api:course-detail',
        lookup_map='course.api.views.CourseViewSet'
    )
    code = serializers.CharField(source='course.code')
    name = serializers.CharField(source='course.name')

    class Meta(AplusModelSerializer.Meta):
        model = CourseInstance
        fields = (
            'url',
            'html_url',
            'code',
            'name',
            'instance_name',
        )


class CourseListField(AlwaysListSerializer, CourseBriefSerializer):
    pass


class CourseUsertagBriefSerializer(AplusModelSerializer):
    """
    BriefSerialzer for course UserTag objects
    """

    class Meta(AplusModelSerializer.Meta):
        model = UserTag
        extra_kwargs = {
            'url': {
                'view_name': 'api:course-usertags-detail',
                'lookup_map': 'course.api.views.CourseUsertagsViewSet',
            }
        }


class CourseSubmissionsBriefSerializer(UserBriefSerializer):
    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        return reverse('api:course-submissiondata-detail', kwargs={
            'course_id': self.context['view'].instance.id,
            'user_id': obj.user.id,
        }, request=self.context['request'])
