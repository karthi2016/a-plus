from django import forms
from django.utils.translation import ugettext_lazy as _

from exercise.models import BaseExercise
from userprofile.models import UserProfile
from course.models import CourseModule


class DeadlineRuleDeviationForm(forms.Form):
    module = forms.ModelMultipleChoiceField(
        queryset=CourseModule.objects.none(),
        required=False
    )
    exercise = forms.ModelMultipleChoiceField(
        queryset=BaseExercise.objects.none(),
        required=False
    )
    submitter = forms.ModelMultipleChoiceField(
        queryset=UserProfile.objects.none(),
    )
    minutes = forms.IntegerField(
        min_value=1,
        help_text=_("Amount of extra time given in minutes."),
    )
    without_late_penalty = forms.BooleanField(
        required=False,
        initial=True,
        label=_("Do not apply late penalty during extra time."),
    )

    def __init__(self, *args, **kwargs):
        course_instance = kwargs.pop('instance')
        super(DeadlineRuleDeviationForm, self).__init__(*args, **kwargs)
        self.fields["module"].widget.attrs["class"] = "search-select"
        self.fields["module"].help_text = ""
        self.fields["module"].queryset = CourseModule.objects.filter(
            course_instance=course_instance
        )
        self.fields["exercise"].widget.attrs["class"] = "search-select"
        self.fields["exercise"].help_text = ""
        self.fields["exercise"].queryset = BaseExercise.objects.filter(
            course_module__course_instance=course_instance
        )
        self.fields["submitter"].widget.attrs["class"] = "search-select"
        self.fields["submitter"].help_text = ""
        self.fields["submitter"].queryset = UserProfile.objects.filter(
            submissions__exercise__course_module__course_instance=course_instance
        ).distinct()
