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
    skip_existing_names = forms.BooleanField(label="Skip rows when name matches", initial=True)

    def save(self):
        assert self.is_valid()

        inserted = 0
        skipped = 0
        f = self.cleaned_data['csv']
        reader = csv.reader((line.decode('utf-8') for line in f))
        EXISTING_NAMES = set(Speaker.objects.values_list('name', flat=True))

        for _ in range(self.cleaned_data['skip_rows']):
            next(reader)  # skip row

        for _row in reader:
            row = BulkUploadRow(*_row)
            if self.cleaned_data['skip_existing_names'] and row.name in EXISTING_NAMES:
                skipped += 1
                continue
            speaker = Speaker.objects.create(
                name=row.name,
                bio=row.bio,
                twitter=row.twitter,
                github=row.github,
                talk_title=row.talk_title,
                talk_description=row.talk_description,
            )

            inserted += 1

        return inserted, skipped
