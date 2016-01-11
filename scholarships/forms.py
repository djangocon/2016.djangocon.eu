from django import forms

from .models import Application


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
