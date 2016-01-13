import argparse
import csv
import sys

from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand
from django.forms.fields import DateTimeField

from cfp.models import Proposal


def datetimetype(s):
    f = DateTimeField()
    try:
        return f.to_python(s)
    except ValidationError as e:
        raise argparse.ArgumentTypeError("Unrecognized datetime format") from e


class Command(BaseCommand):
    help = 'Dump the proposals as CSV to stdout'

    def add_arguments(self, parser):
        parser.add_argument('--since', '-s', type=datetimetype, metavar='SINCE', help="Limit to proposals submitted after SINCE.")

    def handle(self, *args, **options):
        queryset = Proposal.objects.all()
        if options['since']:
            queryset = queryset.filter(submitted_on__gte=options['since'])

        writer = csv.writer(sys.stdout)

        writer.writerow((
            'ID',
            'Title',
            'Description',
            'Audience',
            'Skill level',
            'Notes',
        ))

        for proposal in queryset:
            writer.writerow((
                proposal.pk,
                proposal.title,
                proposal.description,
                proposal.audience,
                proposal.get_skill_level_display(),
                proposal.notes,
            ))
