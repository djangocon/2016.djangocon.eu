import csv

from django.http import StreamingHttpResponse
from django.views.generic import View


class Echo(object):
    """An object that implements just the write method of the file-like
    interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


class StreamingCSVDownloadView(View):
    filename = 'download.csv'

    def get_filename(self):
        return self.filename

    def get_rows(self):
        """
        Return the CSV's rows (ideally as a generator).
        """
        raise NotImplemented

    def get(self, request, *args, **kwargs):
        rows = self.get_rows()
        pseudo_buffer = Echo()
        writer = csv.writer(pseudo_buffer)
        response = StreamingHttpResponse((writer.writerow(row) for row in rows),
                                         content_type="text/csv")
        response['Content-Disposition'] = 'attachment; filename="%s"' % self.get_filename()
        return response
