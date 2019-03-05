import datetime
import json
from datetime import timedelta
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .models import raid_ing, raid, temp


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


# raid_post의 jsonresponse를 만들어주는 함수
def get_resp(params, raid_ing_object, stt):
    if 'raid_level' in params:
        raid_ing_object.update(poke=None, tier=params['raid_level']['value'], s_time=stt)
        return make_simple_text_response(get_raid_board())
    elif 'raid_poke_name' in params:
        poke = raid.objects.filter(poke__name=params['raid_poke_name']['value'])
        raid_ing_object.update(poke=poke[0].id, tier=poke[0].Tier, s_time=stt)
        return make_simple_text_response(get_raid_board())


@csrf_exempt
def post(request):
    json_str = request.body.decode('utf-8')
    received_json_data = json.loads(json_str)
    params = received_json_data['action']['detailParams']
    dt = json.loads(params['sys_plugin_datetime']['value'])['value']
    date = list(map(int, dt[0:10].split('-')))
    time = list(map(int, dt[11:19].split(':')))
    stt = datetime.datetime(date[0], date[1], date[2], time[0], time[1], 0, 0)
    raid_ing_object = raid_ing.objects.filter(gym__name=params['gym_name']['value'])
    return JsonResponse(get_resp(params, raid_ing_object, stt))


def get_raid_board():
    raid_bd = raid_ing.objects.filter(s_time__gte=(timezone.now() + timezone.timedelta(minutes=-46))).order_by('s_time')
    text = ""
    for board in raid_bd:
        raid_obj = ""
        if board.poke:
            raid_obj += str(board.poke)
        else:
            raid_obj += str(board.tier) + "성"
        text += str(board.s_time.strftime('%H:%M')) + "~" + str((board.s_time + timedelta(minutes=45)).strftime('%H:%M')) + " " + str(board.gym.nick) + " " + raid_obj + "\n"

    if text == "":
        return "현재 알려진 레이드가 없습니다! 제보하시겠어요?"
    else:
        return text[:-1]


@csrf_exempt
def board(request):
    return JsonResponse(make_simple_text_response(get_raid_board()))


@csrf_exempt
def mod(request):
    #json data decode
    json_str = request.body.decode('utf-8')
    # 디코드한 json data 풀어보기
    received_json_data = json.loads(json_str)
    # json 파일에서 입력값을 전달해주는 param 접근
    params = received_json_data['action']['detailParams']
    raid_ing_object = raid_ing.objects.filter(gym__name=params['gym_name']['value'])
    if 'sys_plugin_datetime' in params:
        dt = json.loads(params['sys_plugin_datetime']['value'])['value']
        mod_date = list(map(int, dt[0:10].split('-')))
        mod_time = list(map(int, dt[11:19].split(':')))
        st = datetime.datetime(mod_date[0], mod_date[1], mod_date[2], mod_time[0], mod_time[1], 0, 0)
        raid_ing_object.update(s_time=st)
    elif 'raid_poke_name' in params:
        poke = raid.objects.filter(poke__name=params['raid_poke_name']['value'])
        raid_ing_object.update(poke=poke[0].id, tier=poke[0].Tier)

    return JsonResponse(make_simple_text_response(get_raid_board()))