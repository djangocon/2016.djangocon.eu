from django import forms

from .models import Proposal


class CfpForm(forms.ModelForm):
    class Meta:
        model = Proposal
        fields = [
            'name',
            'email',
            'speaker_information',
            'title',
            'description',
            'audience',
            'props',
            'skill_level',
        ]
        widgets = {
            'title': forms.TextInput,
        }
