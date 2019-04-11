from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import raid_ing, raid, gym
from .skills import req_rsp, skillResponse, singleResponse, SkillResponseView, simple_text, simple_image


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
        rep_time = request.params['my_time']['value']
        gym_nicks = [g.nick for g in gym.objects.all()]
        # ~6, 17,18 인문계 / 7~12 이공계 / 13~16, 19~35 기타
        resp = skillResponse()
        liberal_list = list()
        for i in range(6):
            liberal_list.append(singleResponse(gym_nicks[i]).block_button('레이드 장소', {'gym':gym_nicks[i],'raid_time':report_time}, f'{rep_time} {gym_nicks[i]}').form)
        liberal_list.append(singleResponse(gym_nicks[16]).block_button('레이드 장소', {'gym':"한신아파트",'raid_time':report_time}, f'{rep_time} 한신아파트').form)
        liberal_list.append(singleResponse(gym_nicks[17]).block_button('레이드 장소', {'gym':'성복교회','raid_time':report_time}, f'{rep_time} 성복교회').form)
        science_list = list()
        for i in range(6,12):
            science_list.append(singleResponse(gym_nicks[i]).block_button('레이드 장소', {'gym':gym_nicks[i],'raid_time':report_time}, f'{rep_time} {gym_nicks[i]}').form)
        return resp.carousel(liberal_list).carousel(science_list).default


class reportGym(SkillResponseView):
    def make_response(self, request):
        extra_data = request.client_data()
        resp = skillResponse()
        blue_dict = extra_data.copy()
        blue_dict.update({'raid_level':3})
        yellow_dict = extra_data.copy()
        yellow_dict.update({'raid_level':2})
        pink_dict = extra_data.copy()
        pink_dict.update({'raid_level':1})
        blueEgg_list = list(singleResponse("청회색 알").block_button('레이드 포켓몬', blue_dict, f'{extra_data["raid_time"]} {extra_data["gym"]} 5성알').form)
        yellowEgg_list = list(singleResponse("노란 알").block_button('레이드 포켓몬', yellow_dict, f'{extra_data["raid_time"]} {extra_data["gym"]} 노란알').form)
        pinkEgg_list = list(singleResponse("분홍 알").block_button('레이드 포켓몬', pink_dict, f'{extra_data["raid_time"]} {extra_data["gym"]} 분홍알').form)
        for r in raid.objects.filter(Tier=5):
            raid_dict = extra_data.copy()
            raid_dict['poke_name'] = r.poke
            blueEgg_list.append(singleResponse(r.poke).block_button('레이드 포켓몬', raid_dict, f'{extra_data["raid_time"]} {extra_data["gym"]} {r.poke}').form)
        for r in raid.objects.filter(Tier=4):
            raid_dict = extra_data.copy()
            raid_dict['poke_name'] = r.poke
            yellowEgg_list.append(singleResponse(r.poke).block_button('레이드 포켓몬', raid_dict, f'{extra_data["raid_time"]} {extra_data["gym"]} {r.poke}').form)
        for r in raid.objects.filter(Tier=3):
            raid_dict = extra_data.copy()
            raid_dict['poke_name'] = r.poke
            yellowEgg_list.append(singleResponse(r.poke).block_button('레이드 포켓몬', raid_dict, f'{extra_data["raid_time"]} {extra_data["gym"]} {r.poke}').form)
        for r in raid.objects.filter(Tier=2):
            raid_dict = extra_data.copy()
            raid_dict['poke_name'] = r.poke
            pinkEgg_list.append(singleResponse(r.poke).block_button('레이드 포켓몬', raid_dict, f'{extra_data["raid_time"]} {extra_data["gym"]} {r.poke}').form)
        for r in raid.objects.filter(Tier=1):
            raid_dict = extra_data.copy()
            raid_dict['poke_name'] = r.poke
            pinkEgg_list.append(singleResponse(r.poke).block_button('레이드 포켓몬', raid_dict, f'{extra_data["raid_time"]} {extra_data["gym"]} {r.poke}').form)
        return resp.carousel(blueEgg_list).carousel(yellowEgg_list).carousel(pinkEgg_list).default