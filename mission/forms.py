from django import forms
from mission.models import Input
from django.core.exceptions import NON_FIELD_ERRORS


class missionForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Username'}))

    class Meta:
        model = Input
        fields = ('username', 'region', )

        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "Username Already Entered"
            }
        }