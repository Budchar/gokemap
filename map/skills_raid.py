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
        rep_time = request.params['my_time']['value']
        gym_nicks = [g.nick for g in gym.objects.all()]
        # ~6, 17,18 인문계 / 7~12 이공계 / 13~16, 19~35 기타
        resp = skillResponse()
        liberal_list = list()
        for i in range(6):
            liberal_list.append(singleResponse(gym_nicks[i]).block_button('레이드 장소', {'gym':gym_nicks[i],'raid_time':rep_time}, f'{rep_time} {gym_nicks[i]}').form)
        liberal_list.append(singleResponse(gym_nicks[16]).block_button('레이드 장소', {'gym':"한신아파트",'raid_time':rep_time}, f'{rep_time} 한신아파트').form)
        liberal_list.append(singleResponse(gym_nicks[17]).block_button('레이드 장소', {'gym':'성복교회','raid_time':rep_time}, f'{rep_time} 성복교회').form)
        science_list = list()
        for i in range(6,12):
            science_list.append(singleResponse(gym_nicks[i]).block_button('레이드 장소', {'gym':gym_nicks[i],'raid_time':rep_time}, f'{rep_time} {gym_nicks[i]}').form)
        return resp.carousel(liberal_list).carousel(science_list).default


class reportGym(SkillResponseView):
    def make_response(self, request):
        extra_data = request.client_data()
        raid_time = extra_data['raid_time'] if extra_data else request.params['raid_time']['value']
        gym = extra_data['gym'] if extra_data else request.params['gym']['value']
        resp = skillResponse()
        blueEgg_list = list()
        yellowEgg_list = list()
        pinkEgg_list = list()
        for r in raid.objects.filter(Tier=5):
            blueEgg_list.append(singleResponse(r.poke.name).block_button('레이드 포켓몬', {'raid_time':raid_time,'gym':gym,'raid_poke':r.poke.id}, f'{raid_time} {gym} {r.poke.name}').form)
        blueEgg_list.append(singleResponse("오성알").block_button('레이드 포켓몬', {'raid_time': raid_time, 'gym': gym, 'raid_level': 5}, f'{raid_time} {gym} 오성알').form)
        blueEgg_list.append(singleResponse("분홍알").block_button('레이드 포켓몬', {'raid_time': raid_time, 'gym': gym, 'raid_level': 3}, f'{raid_time} {gym} 분홍알').form)
        blueEgg_list.append(singleResponse("노란알").block_button('레이드 포켓몬', {'raid_time': raid_time, 'gym': gym, 'raid_level': 1}, f'{raid_time} {gym} 노란알').form)
        for r in raid.objects.filter(Tier=4):
            yellowEgg_list.append(singleResponse(r.poke.name).block_button('레이드 포켓몬', {'raid_time':raid_time,'gym':gym,'raid_poke':r.poke.id}, f'{raid_time} {gym} {r.poke.name}').form)
        for r in raid.objects.filter(Tier=3):
            yellowEgg_list.append(singleResponse(r.poke.name).block_button('레이드 포켓몬', {'raid_time':raid_time,'gym':gym,'raid_poke':r.poke.id}, f'{raid_time} {gym} {r.poke.name}').form)
        for r in raid.objects.filter(Tier=2):
            pinkEgg_list.append(singleResponse(r.poke.name).block_button('레이드 포켓몬', {'raid_time':raid_time,'gym':gym,'raid_poke':r.poke.id}, f'{raid_time} {gym} {r.poke.name}').form)
        for r in raid.objects.filter(Tier=1):
            pinkEgg_list.append(singleResponse(r.poke.name).block_button('레이드 포켓몬', {'raid_time':raid_time,'gym':gym,'raid_poke':r.poke.id}, f'{raid_time} {gym} {r.poke.name}').form)
        return resp.carousel(blueEgg_list).carousel(yellowEgg_list).carousel(pinkEgg_list).default


class reportPoke(SkillResponseView):
    def make_response(self, request):
        extra_data = request.client_data()
        gym = extra_data['gym'] if extra_data['gym'] else request.params['gym_name']['value']
        time = request.cal_time()
        if ('raid_level' in extra_data) or ('raid_level' in request.params):
            level = extra_data['raid_level'] if extra_data['raid_level'] else request.params['raid_level']['value']
            raid_ing.objects.create(gym=gym, tier=level, s_time=time)
        if ('raid_poke' in extra_data) or ('pokemon' in request.params):
            poke = extra_data['raid_poke'] if extra_data['raid_poke'] else request.params['pokemon']['value']
            poke_obj = raid.objects.filter(poke__id=poke)
            raid_ing.objects.create(gym=gym, poke=poke_obj.id, tier=poke_obj.Tier, s_time=time)
        return self.raid_board()