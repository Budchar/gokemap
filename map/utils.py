import datetime
from datetime import timedelta
from django.utils import timezone
from calendar import HTMLCalendar
from .models import event


class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    def formatday(self, day):
        if day == 0: return '<td></td>'
        else:
            date = datetime.date(self.year, self.month, day)
            events_per_day = event.objects.filter(start_time__lte=date, end_time__gte=date)
            d = ''
            for e in events_per_day:
                d += f'<li> {e.title} </li>'

            return f"<td><span class='date'> {day} </span><ul> {d} </ul></td>"


    def formatweek(self, theweek):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d)
        return f'<tr>{week}</tr>'

    def formatmonth(self, withyear=True):
        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week)}\n'
        cal += f'</table>'
        return cal
