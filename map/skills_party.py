import datetime
import json
from datetime import timedelta
from django.http import JsonResponse
from django.db.models import Sum
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .models import party, raid_ing, partyboard, user


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


def get_party_board():
    text = ""
    # 현재 진행중인 파티 query
    party_ing = party.objects.filter(time__gte=datetime.datetime.now())
    if party_ing:
        # i는 파티순서, p는 파티 오브젝트
        for i, p in enumerate(party_ing):
            # 파티에 속해있는 유저들
            users = partyboard.objects.filter(party=p)
            text += "[팟" + str(i+1) + "] " + p.time.strftime('%H:%M') + " " + str(p.raid.gym.nick) + " " + str(p.raid.poke.poke) +"\n"
            text += "🥇 " + str(int(p.raid.poke.poke.cp_cal(15,15,15,20))) + " /😱 " + str(int(p.raid.poke.poke.cp_cal(10,10,10,20))) +"\n"
            text += "🥇 " + str(int(p.raid.poke.poke.cp_cal(15,15,15,25))) + " /😱 " + str(int(p.raid.poke.poke.cp_cal(10,10,10,25))) + "(날씨부스트)\n\n"
            val_num = users.aggregate(Sum('val'))['val__sum'] if users else 0
            ins_num = users.aggregate(Sum('ins'))['ins__sum'] if users else 0
            mys_num = users.aggregate(Sum('mys'))['mys__sum'] if users else 0
            val_text = "🔥(총 " + str(val_num) + "명)\n" if val_num > 0 else ""
            ins_text = "⚡(총 "+ str(ins_num) + "명)\n" if ins_num > 0 else ""
            mys_text = "❄(총 " + str(mys_num) + "명)\n" if mys_num > 0 else ""
            val_ord = 0
            ins_ord = 0
            mys_ord = 0
            for u in users:
                u_tag = u.tag[0:15] if u.tag else " "
                if u.val > 0:
                    val_ord += 1
                    isarrived = " ✔" if u.arrived == 1 else str(val_ord)
                    val_text += isarrived + ". " + str(u.user.nick)
                    if u.val > 1:
                        val_text += " +" + str(u.val-1)
                    val_text += u_tag + '\n'
                if u.ins > 0:
                    ins_ord += 1
                    isarrived = " ✔" if u.arrived == 1 else str(ins_ord)
                    ins_text += isarrived + ". " + str(u.user.nick)
                    if u.ins > 1:
                        ins_text += " +" + str(u.ins-1)
                    ins_text += u_tag + '\n'
                if u.mys > 0:
                    mys_ord += 1
                    isarrived = " ✔" if u.arrived == 1 else str(mys_ord)
                    mys_text += isarrived + ". " + str(u.user.nick)
                    if u.mys > 1:
                        mys_text += " +" + str(u.mys-1)
                    mys_text += u_tag + '\n'
            text += val_text+mys_text+ins_text+"\n" + str(p.description) + "\n\n"
        return text
    else:
        return "현재 진행중인 파티가 없습니다! 만들어보시는 건 어떨까요?"


class req_rsp:
    def __init__(self, request):
        json_str = request.body.decode('utf-8')
        received_json_data = json.loads(json_str)
        print(received_json_data)
        self.params = received_json_data['action']['detailParams']
        self.user_id = received_json_data['userRequest']['user']['id']


@csrf_exempt
def post(request):
    req = req_rsp(request)
    user_obj = user.objects.filter(kid=req.user_id).first()
    if not user_obj.nick:
        return JsonResponse(make_simple_text_response("명령어 '나는'을 통해 닉네임 먼저 등록해주세요"))
    if not any([user_obj.val, user_obj.ins, user_obj.mys]):
        return JsonResponse(make_simple_text_response("명령어 '내 팀은'을 통해 팀 먼저 등록해주세요"))
    raid_obj = raid_ing.objects.get(gym__name=req.params['gym_name']['value'])
    dt = json.loads(req.params['sys_plugin_datetime']['value'])['value']
    mod_date = list(map(int, dt[0:10].split('-')))
    mod_time = list(map(int, dt[11:19].split(':')))
    st = datetime.datetime(mod_date[0], mod_date[1], mod_date[2], mod_time[0], mod_time[1], 0, 0)

    party_obj = party.objects.filter(raid=raid_obj, time=st)
    if party_obj:
        return JsonResponse(make_simple_text_response("중복된 파티입니다."))
    else:
        party.objects.create(raid=raid_obj, time=st, description=req.params['description']['value'])
        party_bd_obj = party.objects.get(raid__gym__name=req.params['gym_name']['value'], time=st)
        partyboard.objects.create(party=party_bd_obj,user=user_obj,val=user_obj.val,mys=user_obj.mys,ins=user_obj.ins)
        return JsonResponse(make_simple_text_response(get_party_board()))


@csrf_exempt
def board(request):
    return JsonResponse(make_simple_text_response(get_party_board()))


@csrf_exempt
def register(request):
    req = req_rsp(request)
    party_ing = party.objects.filter(time__gte=datetime.datetime.now())
    party_num = int(req.params['party']['value'][1]) - 1
    if len(party_ing) < party_num + 1:
        return JsonResponse(make_simple_text_response("파티는 "+str(len(party_ing))+"개가 진행중입니다"))
    user_id = user.objects.filter(kid=req.user_id).first()
    # if partyboard.objects.filter(party=party_ing[party_num], user=user_id):
    #     return JsonResponse(make_simple_text_response("이미 말씀하신 파티에 속해있는 상태입니다."))
    mys_num = int(req.params.get('mystic', {'value':'미0'})['value'][1])
    val_num = int(req.params.get('valor', {'value':'발0'})['value'][1])
    ins_num = int(req.params.get('instinct', {'value':'인0'})['value'][1])
    user_tag = req.params['sys_text']['value']
    if user_tag == "알릴 말이 없어요":
        user_tag = ""
    if any([mys_num, val_num, ins_num]):
        partyboard.objects.create(party=party_ing[party_num],tag=user_tag,user=user_id,val=val_num,mys=mys_num,ins=ins_num)
    elif any([user_id.val, user_id.mys, user_id.ins]):
        partyboard.objects.create(party=party_ing[party_num],tag=user_tag,user=user_id,val=user_id.val,mys=user_id.mys,ins=user_id.ins)
    else:
        return JsonResponse(make_simple_text_response('제가 '+str(user_id.nick)+'님 팀을 아직 모르겠어요 \n"팟1 미1 참가"처럼 말씀하시거나 \n"내 팀은"이라고 말씀해주세요'))
    return JsonResponse(make_simple_text_response(get_party_board()))


@csrf_exempt
def mod_time(request):
    req = req_rsp(request)
    party_ing = party.objects.filter(time__gte=datetime.datetime.now())
    party_num = int(req.params['party']['value'][1]) - 1
    if len(party_ing) < party_num + 1:
        return JsonResponse(make_simple_text_response("파티는 "+str(len(party_ing))+"개가 진행중입니다"))
    mod_party = party_ing[party_num]
    dt = json.loads(req.params['sys_plugin_datetime']['value'])['value']
    mod_date = list(map(int, dt[0:10].split('-')))
    mod_time = list(map(int, dt[11:19].split(':')))
    st = datetime.datetime(mod_date[0], mod_date[1], mod_date[2], mod_time[0], mod_time[1], 0, 0)
    mod_party.time = st
    mod_party.save()
    return JsonResponse(make_simple_text_response(get_party_board()))


@csrf_exempt
def mod_gym(request):
    req = req_rsp(request)
    party_ing = party.objects.filter(time__gte=datetime.datetime.now())
    party_num = int(req.params['party']['value'][1]) - 1
    if len(party_ing) < party_num + 1:
        JsonResponse(make_simple_text_response("파티는 "+str(len(party_ing))+"개가 진행중입니다"))
    mod_party = party_ing[party_num]
    gym_obj = raid_ing.objects.filter(gym__name=req.params['gym_name']['value']).first()
    mod_party.raid = gym_obj
    mod_party.save()
    return JsonResponse(make_simple_text_response(get_party_board()))


@csrf_exempt
def leave(request):
    req = req_rsp(request)
    user_id = user.objects.filter(kid=req.user_id).first()
    party_ing = party.objects.filter(time__gte=datetime.datetime.now())
    party_num = int(req.params['party']['value'][1]) - 1
    if party_ing:
        user_in_party = partyboard.objects.filter(party=party_ing[party_num], user=user_id)
        if user_in_party:
            user_in_party.delete()
            return JsonResponse(make_simple_text_response(get_party_board()))
        else:
            JsonResponse(make_simple_text_response("해당 파티에 속해있는 상태가 아닙니다."))
    else:
        return JsonResponse(make_simple_text_response("진행중인 파티가 없어요!"))


@csrf_exempt
def arrived(request):
    req = req_rsp(request)
    user_id = user.objects.filter(kid=req.user_id).first()
    party_ing = party.objects.filter(time__gte=datetime.datetime.now())
    party_num = int(req.params['party']['value'][1]) - 1
    if party_ing:
        user_in_party = partyboard.objects.filter(party=party_ing[party_num], user=user_id)
        if user_in_party:
            user_in_party.update(arrived=1)
            return JsonResponse(make_simple_text_response(get_party_board()))
        else:
            JsonResponse(make_simple_text_response("해당 파티에 속해있는 상태가 아닙니다."))
    else:
        return JsonResponse(make_simple_text_response("진행중인 파티가 없어요!"))
