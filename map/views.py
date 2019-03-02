import calendar
import datetime
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views import generic
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_exempt

from .models import raid, pokemon, raid_ing, gym, party
from .utils import Calendar
from .forms import raid_post_form, party_post_form


class IndexView(generic.ListView):
    template_name = 'map/index.html'
    context_object_name = "gym_list"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        d = get_date(self.request.GET.get('day', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context.update({
            'calendar': mark_safe(html_cal),
            'raid_list': raid.objects.order_by('id'),
            'pokemon_list': pokemon.objects.all(),
            'raid_on_list': raid_ing.objects.filter(s_time__gte=(timezone.now() + timezone.timedelta(minutes=-46))),
            'party_list': party.objects.filter(time__gte=timezone.now()),
            # 'raid_form': raid_post_form(),
            # 'party_form': party_post_form(),
        })
        return context

    def get_queryset(self):
        return gym.objects.all()


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        day = 1
        return datetime.datetime.date(year, month, day)
    return datetime.datetime.today()


# def raid_post(request):
#     if request.method == 'POST':
#         instance = get_object_or_404(raid_ing, gym=request.POST['gym'])
#         dt = timezone.localtime().now().strftime("%Y-%m-%d ") + request.POST['s_time']
#         updated_request = request.POST.copy()
#         updated_request.update({'s_time': dt})
#         form = raid_post_form(updated_request or None, instance=instance)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
#
#         else:
#             form = raid_post_form()
#
#         return render(request, 'map/index.html', {'form': form})
#
# def party_post(request):
#     if request.method == 'POST':
#         dt = timezone.localtime().now().strftime("%Y-%m-%d ") + request.POST['p_time']
#         instance = get_object_or_404(raid_ing, id=request.POST['raid'])
#         party.objects.get_or_create(raid=instance, p_time=dt)
#         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))