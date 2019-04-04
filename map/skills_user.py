from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import user
from .skills import req_rsp, skillResponse, singleResponse, simple_text


@csrf_exempt
def user_enroll(request):
    req = req_rsp(request)
    request_user = user.objects.filter(kid=req.user_id)
    if request_user:
        request_user.update(nick=req.params['user_name']['value'])
        return JsonResponse(simple_text(request_user[0].nick+"(으)로 이름을 바꾸셨군요"))
    else:
        user.objects.create(kid=req.user_id, nick=req.params['user_name']['value'])
        return JsonResponse(simple_text(req.params['user_name']['value']+"님 안녕하세요"))


@csrf_exempt
def team_enroll(request):
    req = req_rsp(request)
    mys_num = int(req.params.get('mystic', {'value':'미0'})['value'][1])
    val_num = int(req.params.get('valor', {'value':'발0'})['value'][1])
    ins_num = int(req.params.get('instinct', {'value':'인0'})['value'][1])
    request_user = user.objects.filter(kid=req.user_id)
    # 유저 닉네임이 등록되어있을시
    if request_user:
        request_user.update(kid=req.user_id, val=val_num, ins=ins_num, mys=mys_num)
        return JsonResponse(simple_text(request_user[0].nick+"님 팀 등록 감사합니다"))
    else:
        return JsonResponse(simple_text("별명 등록 먼저 부탁드립니다"))
