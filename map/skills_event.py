import datetime
import json
from datetime import timedelta
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .models import event


def make_simple_text_response(text):
    skill_response_default = {
            "version":"2.0",
            "template":{},
            "context":{},
            "data":{},
        }
    data = {
        "simpleText":{}
        }
    lis = list()
    data['simpleText']['text'] = text
    lis.append(data)
    skill_response_default['template']['outputs'] = lis
    return skill_response_default


class req_rsp:
    def __init__(self, request):
        json_str = request.body.decode('utf-8')
        received_json_data = json.loads(json_str)
        self.params = received_json_data['action']['detailParams']
        self.user_id = received_json_data['userRequest']['user']['id']


@csrf_exempt
def board(request):
    req = req_rsp(request)
    # 시작했고 아직 안 끝난 이벤트
    event_now = event.objects.filter(end_time__gte=timezone.now(), start_time__lte=timezone.now()).order_by('start_time')
    # 아직 시작 안 한 이벤트
    event_upcoming = event.objects.filter(start_time__gte=timezone.now()).order_by('start_time')
    text = ""
    for e in event_now:
        time_delta = e.end_time - timezone.now()
        text += e.title + " " + str(e.end_time.strftime('%m/%d %H:%M')) + "\n" + e.description + "\n" + "종료까지 " + str(time_delta)[0:2] + "일" + str(time_delta)[7:-10] + "\n"
    for e in event_upcoming:
        time_delta = e.start_time - timezone.now()
        text += e.title + " " + str(e.start_time.strftime('%m/%d %H:%M')) + "\n" + e.description + "\n" + "시작까지 " + str(time_delta)[0:2] + "일" + str(time_delta)[7:-10] + "\n"
    return JsonResponse(make_simple_text_response(text))