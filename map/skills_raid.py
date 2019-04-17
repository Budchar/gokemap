from django.http import JsonResponse
from django.db.models import Q
from .models import raid_ing, raid, gym
from .skills import req_rsp, skillResponse, singleResponse, SkillResponseView, simple_text, simple_image


class mod_quarter(SkillResponseView):
    def make_response(self, request):
        resp = skillResponse()
        extra_data = request.client_data()
        gym = raid_ing.objects.filter(id=extra_data['gym_id']).first().gym.nick
        blueEgg_list = list()
        yellowEgg_list = list()
        pinkEgg_list = list()
        blueEgg_list.append(singleResponse(description="시간을 정정하시나요?").block_button("레이드 시간 정정", {'gym': extra_data['gym_id']}, f'{gym} 정정').form)
        for r in raid.objects.filter(Tier=5):
            blueEgg_list.append(singleResponse(r.poke.name).block_button('레이드 포켓몬 정정', {'gym': extra_data['gym_id'], 'raid_poke': r.poke.id}, f'{gym} {r.poke.name} 정정').form)
        blueEgg_list.append(
            singleResponse("오성알").block_button('레이드 포켓몬 정정', {'gym': extra_data['gym_id'], 'raid_level': 5}, f'{gym} 오성알 정정').form)
        blueEgg_list.append(
            singleResponse("분홍알").block_button('레이드 포켓몬 정정', {'gym': extra_data['gym_id'], 'raid_level': 3}, f'{gym} 분홍알 정정').form)
        blueEgg_list.append(
            singleResponse("노란알").block_button('레이드 포켓몬 정정', {'gym': extra_data['gym_id'], 'raid_level': 1}, f'{gym} 노란알 정정').form)
        for r in raid.objects.filter(Tier=4):
            yellowEgg_list.append(singleResponse(r.poke.name).block_button('레이드 포켓몬 정정', {'gym': extra_data['gym_id'], 'raid_poke': r.poke.id}, f'{gym} {r.poke.name} 정정').form)
        for r in raid.objects.filter(Tier=3):
            yellowEgg_list.append(singleResponse(r.poke.name).block_button('레이드 포켓몬 정정', {'gym': extra_data['gym_id'], 'raid_poke': r.poke.id}, f'{gym} {r.poke.name} 정정').form)
        for r in raid.objects.filter(Tier=2):
            pinkEgg_list.append(singleResponse(r.poke.name).block_button('레이드 포켓몬 정정', {'gym': extra_data['gym_id'], 'raid_poke': r.poke.id}, f'{gym} {r.poke.name} 정정').form)
        for r in raid.objects.filter(Tier=1):
            pinkEgg_list.append(singleResponse(r.poke.name).block_button('레이드 포켓몬 정정', {'gym': extra_data['gym_id'], 'raid_poke': r.poke.id}, f'{gym} {r.poke.name} 정정').form)
        return resp.carousel(blueEgg_list).carousel(yellowEgg_list).carousel(pinkEgg_list).default


class raid_board(SkillResponseView):
    def post(self, request):
        return JsonResponse(self.raid_board())


class mod(SkillResponseView):
    def make_response(self, request):
        extra_data = request.client_data()
        raid_ing_id = extra_data['gym']
        raid_ing_object = raid_ing.objects.filter(id=raid_ing_id).first()
        if 'raid_poke' in extra_data:
            poke_object = raid.objects.filter(poke=extra_data['raid_poke']).first()
            raid_ing_object.update(poke=poke_object.id, tier=poke_object.Tier)
        elif 'raid_level' in extra_data:
            raid_ing_object.update(poke=None, tier=extra_data['raid_level'])
        elif 'my_time' in request.params:
            raid_ing_object.update(s_time=request.cal_time())
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
        extra_data = request.client_data() if request.client_data() else {}
        gym_name = request.params['gym_name']['value'] if request.params else extra_data['gym']
        gym_obj = gym.objects.filter(Q(name=gym_name)|Q(nick=gym_name)).first()
        time = request.cal_time()
        if ('raid_level' in extra_data) or ('raid_level' in request.params):
            level = request.params['raid_level']['value'] if request.params else extra_data['raid_level']
            raid_ing.objects.create(gym=gym_obj, poke=None, tier=level, s_time=time)
        if ('raid_poke' in extra_data) or ('pokemon' in request.params):
            poke = request.params['pokemon']['value'] if request.params else extra_data['raid_poke']
            poke_obj = raid.objects.filter(poke__id=poke).first()
            raid_ing.objects.create(gym=gym_obj, poke=poke_obj, tier=poke_obj.Tier, s_time=time)
        return self.raid_board()