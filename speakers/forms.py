import csv
from collections import namedtuple

from django import forms

from .models import Speaker


BulkUploadRow = namedtuple('BulkUploadRow', [
    'timestamp',
    'name',
    'bio',
    'picture_url',
    'twitter',
    'github',
    'talk_title',
    'talk_description',
    'hotel_nights',
    'travel_companion',
    'room_share',
])


class BulkUploadForm(forms.Form):
    csv = forms.FileField(label="Your CSV file")
    skip_rows = forms.IntegerField(label="Number of rows to skip", initial=1)

    def save(self):
        assert self.is_valid()

        inserted = 0
        f = self.cleaned_data['csv']
        reader = csv.reader((line.decode('utf-8') for line in f))

        for _ in range(self.cleaned_data['skip_rows']):
            next(reader)  # skip row

        for _row in reader:
            row = BulkUploadRow(*_row)
            speaker = Speaker.objects.create(
                name=row.name,
                bio=row.bio,
                twitter=row.twitter,
                github=row.github,
                talk_title=row.talk_title,
                talk_description=row.talk_description,
            )

            inserted += 1

        return inserted
