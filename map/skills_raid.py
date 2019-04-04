from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import raid_ing, raid, gym
from .skills import req_rsp, skillResponse, singleResponse, SkillResponseView, simple_text


class raid_post(SkillResponseView):
    def make_response(self, request):
        params = request.params
        st = request.get_time()
        raid_ing_object = raid_ing.objects.filter(gym__name=params['gym_name']['value'])
        if 'raid_level' in params:
            raid_ing_object.update(poke=None, tier=params['raid_level']['value'], s_time=st)
        elif 'raid_poke_name' in params:
            poke = raid.objects.filter(poke__name=params['raid_poke_name']['value'])
            raid_ing_object.update(poke=poke[0].id, tier=poke[0].Tier, s_time=st)
        return self.raid_board()


class raid_board(SkillResponseView):
    def post(self, request):
        return JsonResponse(self.raid_board())


@csrf_exempt
def mod(request):
    params = req_rsp(request).params
    raid_ing_object = raid_ing.objects.filter(gym__name=params['gym_name']['value'])
    if 'sys_plugin_datetime' in params:
        st = params.get_time()
        raid_ing_object.update(s_time=st)
    elif 'raid_poke_name' in params:
        poke = raid.objects.filter(poke__name=params['raid_poke_name']['value'])
        raid_ing_object.update(poke=poke[0].id, tier=poke[0].Tier)

    return JsonResponse(simple_text(get_raid_board()))


class reportFire(SkillResponseView):
    def make_response(self, request):
        gym_nicks = [g.nick for g in gym.objects.all()]
        title = simple_text("체육관 이름을 입력해주세요")
        text = simple_text("<체육관 목록>\n" + ", ".join(gym_nicks))
        resp = skillResponse()
        resp.input(title)
        return resp.input(text)
