from math import ceil
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.models import Site


class CsvToTxt(object):
    """
    Convert CSV string to fixed width text table. Supports multi-line rows, column width limits, and creates a header row automatically
    @author Tony Landis
    @link http://www.tonylandis.com
    @license GPL
    """

    cs = []
    rs = []
    keys = []
    mH = 3
    mW = 200
    pcen = "+"
    prow = "-"
    pcol = "|"
    pcolm = ":"
    nline = False

    def __init__(self, source, delimiter=";"):
        x = 0
        self.rows = []
        for row in source.split("\n")[:]:
            self.rs.append(x)
            self.rs[x] = 1
            cols = row.split(delimiter)
            self.rows.append(cols)
            if(x == 0):
                self.keys = cols
                for index in range(len(cols)):
                    self.cs.append(index)
            for index, item in enumerate(cols):
                self.setMax(x, index, item)
            x += 1

    def setMax(self, x, y, data):
        h = 1
        w = len(data)
        if w > self.mW:
            h = ceil(w % self.mH)
            w = self.mW
        if self.cs[y] < w:
            self.cs[y] = w
        if self.rs[x] < h:
            self.rs[x] = h

    def printLine(self, nl=True):
        if self.nline:
            return self.nline
        else:
            self.nline = self.pcen
        for len in self.cs[:]:
            self.nline += self.prow.rjust(len, self.prow) + \
                self.prow + self.prow + self.pcen
        return self.nline

    def printRow(self, rowKey):
        string = ''
        line = 0
        while line < self.rs[rowKey]:
            start = self.mW * (line)
            if line > 0:
                pcol = self.pcolm
                end = self.mW + start
            else:
                pcol = self.pcol
                end = self.mW
            string = pcol
            for index, item in enumerate(self.rows[rowKey]):
                string += " "
                string += item[start:end].ljust(self.cs[index], ' ')
                string += " " + pcol
            return string
            line += 1
        return string

    def render(self):
        out = ""
        for i in range(len(self.rows)):
            out += self.printRow(i)
            out += " \n"
        return out


def send_email_html(subject, from_email, to,
                    template_name, context={}, *args, **kwargs):
    context['MEDIA_URL'] = settings.MEDIA_URL
    context['current_site'] = Site.objects.get_current()
    html_content = render_to_string(template_name, context)
    msg = EmailMessage(subject, html_content, from_email, to, *args, **kwargs)
    msg.content_subtype = "html"
    return msg.send()
