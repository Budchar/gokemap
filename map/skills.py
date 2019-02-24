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

skill_response_default={
        "version":"2.0",
        "template":{},
        "context":{},
        "data":{},
    }


@csrf_exempt
def raid_post(request):
    # print('META', request.META)
    json_str = ((request.body).decode('utf-8'))
    received_json_data = json.loads(json_str)
    params = received_json_data['action']['detailParams']
    dt = json.loads(params['sys_time']['value'])
    time = list(map(int, dt['time'].split(':')))
    date = list(map(int, dt['date'].split('-')))
    stt = datetime.datetime(date[0], date[1], date[2], time[0], time[1], 0, 0)
    if datetime.datetime.now().time() > datetime.time(12):
        stt += timedelta(hours=12)
    if 'raid_level' in params:
        raid_ing.objects.filter(gym__name=params['gym_name']['value']).update(poke=None, tier=params['raid_level']['value'], s_time=stt)
        return JsonResponse({
            'version':"2.0",
            'template':{
                'output':[
                    {'simpleText':{
                        'text': 'receive ok'
                        }
                    }
                    ]
                }
            })
    elif 'raid_poke_name' in params:
        poke = raid.objects.filter(poke__name=params['raid_poke_name']['value'])
        raid_ing.objects.filter(gym__name=params['gym_name']['value']).update(poke=poke[0].id, s_time=stt)
        return JsonResponse({
            'version':"2.0",
            'template':{
                'output':[
                    {'simpleText':{
                        'text': 'receive ok'
                        }
                    }
                    ]
                }
            })
    else: return JsonResponse({
            'version':"2.0",
            'template':{
                'output':[
                    {'simpleText':{
                        'text': 'no poke or level'
                        }
                    }
                    ]
                }
            })


@csrf_exempt
def raid_board(request):
    response = skill_response_default
    data = {
        "simpleText":{}
        }
    lis = list()
    text = ""
    raid = raid_ing.objects.filter(s_time__gte=(timezone.now() + timezone.timedelta(minutes=-46)))
    for i in raid:
        raid_obj = ""
        if i.poke:
            raid_obj += str(i.poke)
        else:
            raid_obj += str(i.tier) + "성"
        text += str(i.gym) + " " + raid_obj + " " + str(i.s_time.strftime('%H:%M')) + "~" + str((i.s_time + timedelta(minutes=45)).strftime('%H:%M'))+"\n"
    if text == "":
        text += "현재 알려진 레이드가 없습니다! 제보하시겠어요?"
    data['simpleText']['text'] = text
    lis.append(data)
    response['template']['outputs'] = lis
    return JsonResponse(response)