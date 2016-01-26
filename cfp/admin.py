import itertools

from django.contrib import admin
from django.contrib import messages
from django.shortcuts import redirect
from django.utils import timezone

from djangocon.csvutils import get_streaming_csv_response
from .models import Proposal


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


def select_proposals(modeladmin, request, queryset):
    """
    Mark the given proposal(s) as selected
    """
    updated = queryset.update(selected=True)
    messages.success(request, "%s proposals were marked as selected" % updated)
    return redirect('admin:cfp_proposal_changelist')

select_proposals.short_description = "Mark selected proposals as selected"


@admin.register(Proposal)
class ProposalAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'title']
    search_fields = ['name', 'email', 'title']
    list_per_page = 200
    actions = [download_csv, select_proposals]
    list_filter = ['selected']
