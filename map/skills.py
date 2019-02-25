import datetime
import json
import copy
from datetime import timedelta
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .models import raid_ing, raid


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


# 레이드 시작 가능 시간을 구해주는 함수
def get_datetime(time, date):
    # input을 datetime형식으로 변환
    st = datetime.datetime(date[0], date[1], date[2], time[0], time[1], 0, 0)
    # 12시 이후에 12시간 방식으로 제보하면 24시간 방식으로 변환해줌
    if (datetime.datetime.now().time() > datetime.time(12)) and (st.time() < datetime.time(12)):
        st += timedelta(hours=12)
        # 0시의 경우에는 하루가 지나야함으로 12시간 추가
        if st.time() == datetime.time(0):
            st += timedelta(hours=12)

    return st


# raid_post의 jsonresponse를 만들어주는 함수
def get_resp(params, raid_ing_object, stt):
    if 'raid_level' in params:
        raid_ing_object.update(poke=None, tier=params['raid_level']['value'], s_time=stt)
        return make_simple_text_response('raid level receive ok')
    elif 'raid_poke_name' in params:
        poke = raid.objects.filter(poke__name=params['raid_poke_name']['value'])
        raid_ing_object.update(poke=poke[0].id, s_time=stt)
        return make_simple_text_response('raid poke receive ok')
    else: return make_simple_text_response('no raid level or poke')


@csrf_exempt
def raid_post(request):
    json_str = (request.body.decode('utf-8'))
    received_json_data = json.loads(json_str)
    params = received_json_data['action']['detailParams']
    dt = json.loads(params['sys_time']['value'])
    time = list(map(int, dt['time'].split(':')))
    date = list(map(int, dt['date'].split('-')))
    stt = get_datetime(time, date)
    raid_ing_object = raid_ing.objects.filter(gym__name=params['gym_name']['value'])
    return JsonResponse(get_resp(params, raid_ing_object, stt))


def get_raid_board(raid_bd):
    text = ""
    for i in raid_bd:
        raid_obj = ""
        if i.poke:
            raid_obj += str(i.poke)
        else:
            raid_obj += str(i.tier) + "성"
        text += str(i.s_time.strftime('%H:%M')) + "~" + str((i.s_time + timedelta(minutes=45)).strftime('%H:%M')) + " " + str(i.gym) + " " + raid_obj + "\n"
    if text == "":
        text += "현재 알려진 레이드가 없습니다! 제보하시겠어요?"
    return text


@csrf_exempt
def raid_board(request):
    raid_bd = raid_ing.objects.filter(s_time__gte=(timezone.now() + timezone.timedelta(minutes=-46))).order_by('s_time')
    return JsonResponse(make_simple_text_response(get_raid_board(raid_bd)))
