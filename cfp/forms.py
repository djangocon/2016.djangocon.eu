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
            'mentoring',
            'notes',
        ]
        labels = {
            'name': 'Your name',
            'email': 'Your email',
            'speaker_information': 'Tell us about you',
            'title': 'Your talk\'s title',
            'description': 'Description of your talk',
            'audience': 'What do you think the audience will get from your talk',
            'props': 'Do you have specific requirements for your talk',
            'skill_level': 'Who is the intended audience for your talk',
            'notes': 'Anything else you\'d like to share with us',
            'mentoring': 'Do you want a mentor',
        }
        help_texts = {
            'props': 'Will you need sound, an extra table on stage, a smoke machine, ...',
            'mentoring': 'We can put you in touch with an experience speaker from the Django community who will help you prepare your presentation',
        }
        widgets = {
            'title': forms.TextInput,
        }
