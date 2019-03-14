import json
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


def make_basic_card(title, time, extra, imgurl):
    card_form = {
        'title': title,
        'description': time,
        'thumbnail':{
            'imageUrl': imgurl,
        },
        'buttons': [
            {
                'action': 'block',
                'label': "상세 정보",
                'messageText': '이벤트 상세 정보',
                'blockId': '5c89f9ac5f38dd4767218f9d',
                'extra': {
                    'data': extra,
                }
            },
        ]
    }
    return card_form


def make_carousel(card_list):
    skill_response_default = {
            "version":"2.0",
            "template":{},
            "context":{},
            "data":{},
        }
    data = {
        "carousel":{
            'type': "basicCard",
            'items': card_list,
        }
    }
    lis = list()
    lis.append(data)
    skill_response_default['template']['outputs'] = lis
    return skill_response_default


class req_rsp:
    def __init__(self, request):
        json_str = request.body.decode('utf-8')
        received_json_data = json.loads(json_str)
        self.params = received_json_data['action']['detailParams']
        self.user_id = received_json_data['userRequest']['user']['id']
        self.client_data = received_json_data['action']['clientExtra']['data']


@csrf_exempt
def board(request):
    # 시작했고 아직 안 끝난 이벤트
    event_now = event.objects.filter(end_time__gte=timezone.now(), start_time__lte=timezone.now()).order_by('start_time')
    # 아직 시작 안 한 이벤트
    event_upcoming = event.objects.filter(start_time__gte=timezone.now()).order_by('start_time')
    card_list = list()
    for e in event_now:
        time_delta = e.end_time - timezone.now()
        e_time = str(e.end_time.strftime('%m/%d %H:%M')) + " 종료" + "(종료까지 " + str(time_delta)[0:2] + "일" + str(time_delta)[7:-10] + ")"
        card_list.append(make_basic_card(e.title, e_time, e.id, e.img_url))
    for e in event_upcoming:
        time_delta = e.start_time - timezone.now()
        e_time = str(e.start_time.strftime('%m/%d %H:%M')) + " 시작" + "(시작까지 " + str(time_delta)[0:2] + "일" + str(time_delta)[7:-10] + ")"
        card_list.append(make_basic_card(e.title, e_time, e.id, e.img_url))
    return JsonResponse(make_carousel(card_list))


@csrf_exempt
def detail(request):
    req = req_rsp(request)
    event_obj = event.objects.filter(id=req.client_data)
    # 이미 시작한 이벤트
    if event_obj.start_time > timezone.now():
        time_delta = event_obj.end_time - timezone.now()
        e_time = str(event_obj.end_time.strftime('%m/%d %H:%M')) + " 종료" + "(종료까지 " + str(time_delta)[0:2] + "일" + str(time_delta)[7:-10] + ")"
        text = event_obj.title + "\n" + e_time + "\n\n" + event_obj.description
        return JsonResponse(make_simple_text_response(text))
    else:
        time_delta = event_obj.start_time - timezone.now()
        e_time = str(event_obj.start_time.strftime('%m/%d %H:%M')) + " 시작" + "(시작까지 " + str(time_delta)[0:2] + "일" + str(time_delta)[7:-10] + ")"
        text = event_obj.title + "\n" + e_time + "\n\n" + event_obj.description
        return JsonResponse(make_simple_text_response(text))
