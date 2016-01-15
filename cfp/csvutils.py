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


def get_streaming_csv_response(rows, filename):
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    response = StreamingHttpResponse((writer.writerow(row) for row in rows),
                                     content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="%s"' % filename
    return response


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
        return get_streaming_csv_response(self.get_rows(), filename=self.get_filename())
