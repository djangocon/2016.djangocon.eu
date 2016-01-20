import itertools

from django.contrib import admin
from django.utils import timezone

from .models import Proposal
from .csvutils import get_streaming_csv_response


def download_csv(modeladmin, request, queryset):
    """
    Download the given proposal queryset as a CSV.
    """
    header = Proposal.as_csv_row.HEADER
    data_rows = (proposal.as_csv_row() for proposal in queryset)

    rows = itertools.chain([header], data_rows)
    filename = 'proposals-{:%Y%m%d_%H%M%S}.csv'.format(timezone.now())
    return get_streaming_csv_response(rows, filename=filename)

download_csv.short_description = "Download selected proposals as CSV"


@admin.register(Proposal)
class ProposalAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'title']
    list_per_page = 200
    actions = [download_csv]
