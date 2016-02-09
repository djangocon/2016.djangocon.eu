from django.core.mail import send_mail
from django import forms
from django.template import Context, Template

from .models import Proposal, WorkshopProposal

CONFIRMATION_EMAIL_TEMPLATE = """Hi {{ form.name.value }},


This is an automated email to confirm that we have received your application
for the DjangoCon Europe 2016 call for workshops.


Here is the data you submitted to us:
{% for field in form %}{{ field.label }}:
{{ field.value }}


{% endfor %}
We will contact you with the result of your application around February 24th.
In the meantime, feel free to contact us if you have any questions: 2016@djangocon.eu


All the best,
The DjangoCon Europe 2016 team.
"""


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

    def __init__(self, *args, **kwargs):
        super(CfpForm, self).__init__(*args, **kwargs)
        for f in self.fields.values():
            if not f.required:
                continue
            f.widget.attrs.setdefault('required', True)
            f.label = '{} *'.format(f.label)


class WorkshopForm(CfpForm):
    class Meta(CfpForm.Meta):
        model = WorkshopProposal
        labels = {
            'name': 'Your name',
            'email': 'Your email',
            'speaker_information': 'Tell us about you',
            'title': 'Workshop title',
            'description': 'Workshop description',
            'audience': 'What will attendees gain from your workshop?',
            'props': 'Do you have any special requirements for your workshop?',
            'skill_level': 'Who is the intended audience for your workshop',
            'notes': 'Anything else you\'d like to share with us',
            'mentoring': 'Do you need any help with your workshop?',
        }
        help_texts = {
            'props': 'Tech, seating arrangement, whiteboards, anything else?',
            'mentoring': 'You can always contact us with questions, even if you don’t think you need help right now.',
        }

    def save(self, commit=True):
        application = super(WorkshopForm, self).save(commit)
        self.send_confirmation_email()
        return application

    def send_confirmation_email(self):
        subject = '[DjangoCon Europe 2016] Confirmation of your workshop proposal'
        body = Template(CONFIRMATION_EMAIL_TEMPLATE).render(Context({'form': self}))
        to = self.cleaned_data['email']
        from_ = 'DjangoCon Europe 2016 <2016@djangocon.eu>'
        return send_mail(subject, body, from_, [to])
