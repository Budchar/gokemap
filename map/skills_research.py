import datetime
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .models import temp, research
from .skills import req_rsp, skillResponse, singleResponse, simple_text, SkillResponseView


@csrf_exempt
def post(request):
    req = req_rsp(request)
    if (req.user_id == 'b32a22d3306d1fd49149991ec0293f580186b459ec3bd6d29a0e36547409d8385c') or (req.user_id == '457ae6a6448028ad73d2cf1a35ab3eac4c18334edf16d13446a114bcf9476ea951'):
        temp.objects.update(id=1, date=datetime.datetime.now(), description=req.params['sys_text']['value'])
        return JsonResponse(simple_text("리서치 제보 감사합니다"))
    else:
        return JsonResponse(simple_text("현재 리서치 제보는 몇몇분 한정으로 기능하고 있습니다."))


class board(SkillResponseView):
    def make_response(self, request):
        research_objs = research.objects.all()
        research_text = ""
        for research_obj in research_objs:
            research_text += f"{research_obj.todo}\n -{research_obj.rwd}\n"

        return skillResponse.input(singleResponse("리서치 목록", f"{research_text}").share().card())

# @csrf_exempt
# def board(request):
    # research_bd = temp.objects.filter(date=(timezone.now().date())).first()
    # research_objs = research.objects.all()
    # rsch = getattr(research_bd, "description", "오늘은 리서치가 아직 제보되지 않았네요 ㅠㅁㅠ")
    # research_text = ""
    # for research_obj in research_objs:
    #     research_text += f"{research_obj.todo}\n -{research_obj.rwd}\n"
    #
    # return JsonResponse(simple_text(research_text))
