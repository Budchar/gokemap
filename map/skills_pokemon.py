from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import itertools
import math
from .models import pokemon, poke_move, chargeMove, fastMove, move
from .skills import req_rsp, skillResponse, singleResponse, simple_text


def weak(type_1, type_2=False):
    type_matrix = {
        # 노말 기준 맞을때 type_matrix[노말][전 속성], 때릴때 type_matrix[전 속성][노말]
        '노말': {
            '고스트': 0.39,
            '격투': 1.6
        },
        '격투': {
            '벌레': 0.625, '바위': 0.625, '악': 0.625,
            '비행': 1.6, '에스퍼': 1.6, '페어리': 1.6
        },
        '독': {
            '격투': 0.625, '독': 0.625, '벌레': 0.625, '풀': 0.625, '페어리': 0.625,
            '땅': 1.6, '에스퍼': 1.6
        },
        '땅': {
            '전기': 0.39,
            '독': 0.625, '바위': 0.625,
            '물': 1.6, '풀': 1.6, '얼음': 1.6
        },
        '비행': {
            '땅': 0.39,
            '격투': 0.625, '벌레': 0.625, '풀': 0.625,
            '바위': 1.6, '전기': 1.6, '얼음': 1.6
        },
        '벌레': {
            '격투': 0.625, '땅': 0.625, '풀': 0.625,
            '비행': 1.6, '바위': 1.6, '불꽃': 1.6,
        },
        '바위': {
            '노말': 0.625, '독': 0.625, '비행': 0.625, '불꽃': 0.625,
            '격투': 1.6, '땅': 1.6, '강철': 1.6, '물': 1.6, '풀': 1.6
        },
        '고스트': {
            '노말': 0.39, '격투': 0.39,
            '독': 0.625, '벌레': 0.625,
            '고스트': 1.6, '악': 1.6
        },
        '강철': {
            '독': 0.39,
            '노말': 0.625, '비행': 0.625, '벌레': 0.625, '바위': 0.625, '강철': 0.625, '풀': 0.625, '얼음': 0.625, '에스퍼': 0.625,
            '드래곤': 0.625, '페어리': 0.625,
            '격투': 1.6, '땅': 1.6, '불꽃': 1.6
        },
        '불꽃': {
            '벌레': 0.625, '강철': 0.625, '불꽃': 0.625, '풀': 0.625, '얼음': 0.625, '페어리': 0.625,
            '땅': 1.6, '바위': 1.6, '물': 1.6
        },
        '물': {
            '강철': 0.625, '불꽃': 0.625, '물': 0.625, '얼음': 0.625,
            '전기': 1.6, '풀': 1.6
        },
        '전기': {
            '비행': 0.625, '강철': 0.625, '전기': 0.625,
            '땅': 1.6
        },
        '풀': {
            '땅': 0.625, '물': 0.625, '전기': 0.625, '풀': 0.625,
            '독': 1.6, '비행': 1.6, '벌레': 1.6, '불꽃': 1.6, '얼음': 1.6
        },
        '얼음': {
            '얼음': 0.625,
            '격투': 1.6, '바위': 1.6, '불꽃': 1.6, '강철': 1.6
        },
        '에스퍼': {
            '격투': 0.625, '에스퍼': 0.625,
            '벌레': 1.6, '고스트': 1.6, '악': 1.6
        },
        '드래곤': {
            '불꽃': 0.625, '물': 0.625, '전기': 0.625, '풀': 0.625,
            '얼음': 1.6, '드래곤': 1.6, '페어리': 1.6,
        },
        '악': {
            '에스퍼': 0.39,
            '고스트': 0.625, '악': 0.625,
            '격투': 1.6, '벌레': 1.6, '페어리': 1.6
        },
        '페어리': {
            '드래곤': 0.39,
            '격투': 0.625, '벌레': 0.625, '악': 0.625,
            '독': 1.6, '강철': 1.6

        }
    }
    # 첫번째 타입 약점
    if type_2:
        return {k: type_matrix[type_1].get(k, 1) * type_matrix[type_2].get(k, 1) for k in
                type_matrix[type_1].keys() | type_matrix[type_2]}
    else:
        return type_matrix[type_1]


def weather(type_1, type_2=False):
    weather_match = {
        '풀': '☀', '불꽃': '☀', '땅': '☀', '노말': '⛅', '바위': '⛅', '페어리': '☁', '격투': '☁', '독': '☁',
        '물': '☂', '전기': '☂', '벌레': '☂', '강철': '⛄', '얼음': '⛄', '비행': '🌪', '드래곤': '🌪', '에스퍼': '🌪', '고스트': '🌫',
        '악': '🌫'
    }
    set_weather = set()
    if type_2:
        set_weather.update(weather_match[type_1], weather_match[type_2])
        return set_weather
    else:
        return weather_match[type_1]


def dps(poke_obj, c):
    type_choice = {'Normal': '노말', 'Fire': '불꽃', 'Water': '물', 'Grass': '풀', 'Electric': '전기',
                   'Ice': '얼음', 'Fighting': '격투', 'Poison': '독', 'Ground': '땅', 'Flying': '비행', 'Psychic': '에스퍼',
                   'Bug': '벌레', 'Rock': '바위', 'Ghost': '고스트', 'Dragon': '드래곤', 'Dark': '악', 'Steel': '강철',
                   'Fairy': '페어리'}
    fm = c[0]
    cm = c[1]
    fm_stab = 1.25 if type_choice[fm.move.Move_Type] == poke_obj.type_1 or type_choice[fm.move.Move_Type] == poke_obj.type_2 else 1
    cm_stab = 1.25 if type_choice[cm.move.Move_Type] == poke_obj.type_1 or type_choice[
        cm.move.Move_Type] == poke_obj.type_2 else 1
    fm_dmg = math.floor(poke_obj.atk/200*fm.move.PVE_Base_Power*fm_stab)+1
    cm_dmg = (math.floor(poke_obj.atk/200*cm.move.PVE_Base_Power*cm_stab)+1)*chargeMove.objects.filter(default_info=cm.move).first().PVE_Charge_Energy
    dmg = fm_dmg + cm_dmg
    return dmg


@csrf_exempt
def info(request):
    req = req_rsp(request)
    return JsonResponse()


@csrf_exempt
def detail(request):
    req = req_rsp(request)
    poke_sort_cp = pokemon.objects.all()
    poke_obj = pokemon.objects.filter(num=req.params['pokemon']['value']).first()
    # 전체 포켓몬에서 cp순으로 sorted함수를 적용하고 이를 index method를 통해 찾고자 하는 query object를 찾는다.
    fast_move = poke_move.objects.filter(pokemon=poke_obj,move__Move_Category='Fast Move')
    charge_move = poke_move.objects.filter(pokemon=poke_obj, move__Move_Category='Charge Move')
    move_comb = [f"{c[0].move.name}/{c[1].move.name} dps:{dps(poke_obj, c)}" for c in list(itertools.product(fast_move, charge_move))]
    cp_rank = sorted(poke_sort_cp, key=lambda p: p.cp_cal(15, 15, 15, 25), reverse=True).index(poke_obj)
    types = poke_obj.type_1 + "/" + poke_obj.type_2 if poke_obj.type_2 != 'NULL' else poke_obj.type_1
    weak_dict = weak(poke_obj.type_1.strip(), poke_obj.type_2.strip()) if poke_obj.type_2 != 'NULL' else weak(poke_obj.type_1)
    weather_set = weather(poke_obj.type_1.strip(), poke_obj.type_2.strip()) if poke_obj.type_2 != 'NULL'else weather(poke_obj.type_1)
    weak_txt = ""
    for key, value in sorted(weak_dict.items(), key=lambda p: p[1], reverse=True):
        if value > 1:
            if weak_txt.find(str(round(value, 2))) > 0:
                weak_txt = weak_txt[:weak_txt.find(str(round(value, 2)))-1] + f', {key}' + weak_txt[weak_txt.find(str(round(value, 2)))-1:]
            else:
                weak_txt += f'{key}({round(value, 2)}배) '
    output = f"{poke_obj.name} (#{poke_obj.num[:3] if len(poke_obj.num)>3 else poke_obj.num}) {', '.join(weather_set)}\n\n" + f"타입 {types}\n" + f"약점 {weak_txt}\n" +f"공격 {poke_obj.atk}/방어 {poke_obj.df}/체력 {poke_obj.stm}\n\n" + f"CP(전체 {cp_rank+1}위)\n" + f"Lv20.💯{math.floor(poke_obj.cp_cal(15,15,15,20))}\n" + f"Lv25.💯{math.floor(poke_obj.cp_cal(15,15,15,25))}\n"
    output += f"\n스킬\n" + "\n".join(move_comb)
    return JsonResponse(simple_text(output))