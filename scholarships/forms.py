from django.core.mail import send_mail
from django import forms
from django.template import Context, Template

from .models import Application

CONFIRMATION_EMAIL_TEMPLATE = """Hi {{ form.name.value }},


This is an automated email to confirm that we have received your application
for the DjangoCon Europe 2016 scholarship program.


Here is the data you submitted to us:
{% for field in form %}{{ field.label }}:
{{ field.value }}


{% endfor %}
We will contact you with the result of your application on February 1st.
In the meantime, feel free to contact us if you have any questions: 2016@djangocon.eu


All the best,
The DjangoCon Europe 2016 team.
"""


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = [
            'name',
            'email',
            'python_django',
            'why',
            'financial_assistance',
            'location',
            'notes',
        ]
        labels = {
            'name': 'Your name',
            'email': 'Your email',
            'python_django': 'What do you do with Python or Django? ',
            'why': 'Why do you want to attend DjangoCon Europe',
            'financial_assistance': 'Do you need financial assistance to attend the conference? If so, please provide an estimate of costs for your travel and accommodation in Budapest during the conference.',
            'location': 'Where do you live',
            'notes': 'Anything else you\'d like to tell us',
        }
        help_texts = {
            'python_django': 'If you don\'t already use it, let us know what you plan to do with it',
            'financial_assistance': 'Provide an estimate in <strong>Euros</strong>',
            'location': 'City <strong>and country</strong>'
        }

    def __init__(self, *args, **kwargs):
        super(ApplicationForm, self).__init__(*args, **kwargs)
        for f in self.fields.values():
            if not f.required:
                continue
            f.widget.attrs.setdefault('required', True)
            f.label = '{} *'.format(f.label)

    def save(self, commit=True):
        application = super(ApplicationForm, self).save(commit)
        self.send_confirmation_email()
        return application

    def send_confirmation_email(self):
        subject = '[DjangoCon Europe 2016] Confirmation of your scholarship application'
        body = Template(CONFIRMATION_EMAIL_TEMPLATE).render(Context({'form': self}))
        to = self.cleaned_data['email']
        from_ = 'DjangoCon Europe 2016 <2016@djangocon.eu>'
        return send_mail(subject, body, from_, [to])
