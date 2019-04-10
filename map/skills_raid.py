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


class mod(SkillResponseView):
    def make_response(self, request):
        params = request.params
        raid_ing_object = raid_ing.objects.filter(gym__name=params['gym_name']['value'])
        if 'sys_plugin_datetime' in params:
            st = params.get_time()
            raid_ing_object.update(s_time=st)
        elif 'raid_poke_name' in params:
            poke = raid.objects.filter(poke__name=params['raid_poke_name']['value'])
            raid_ing_object.update(poke=poke[0].id, tier=poke[0].Tier)
        return self.raid_board()


class reportFire(SkillResponseView):
    def make_response(self, request):
        report_time = request.cal_time()
        gym_nicks = [g.nick for g in gym.objects.all()]
        # ~6, 17,18 인문계 / 7~12 이공계 / 13~16, 19~35 기타
        resp = skillResponse()
        resp.input(singleResponse(title="레이드 전체 지도", thumbnail="https://0d257daf-a-62cb3a1a-s-sites.googlegroups.com/site/koreapogoguide/home/5-hwagjang-jeonche-jido/%EC%88%98%EC%A0%95%EB%90%A8_Screenshot_1.png?attachauth=ANoY7cpQyv_p7PpTemnduS1OAT61b034tzSnnUCam300-wgzgiirP4JQ7kjrI2o3Ye4TqL5_rWgwqj8kvZVbU07JispVOJLU-Pq_6iMIR0TlidJru6uA82CHp2ehEDc3UE8oAJAes3URPjvb1Y5Abql_fW_5D2bnSTLhY0mEvZmlZRCfsK6oObmAlv2ur0NhoxuDPgYfnDaKaGnqio9P1r2a7f9WZQc29sS7rligPbMywrUxwNau9z4d_vhSr_vR_p0OK7lV4wx5SH9hWFjs4OHCoJBpkaQYFLEhCSl86Jc0jqAFeA0L1gU%3D&attredirects=0").form)
        return resp.default
