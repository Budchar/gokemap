import requests, bs4
print('Connecting sys...')
import sys
# sys.path.append('/home/budcha/gokemap') #서버용
sys.path.append('C:\\Users\\leesehoon\\Desktop\\Gokemap\\gokemap')#테스트용
print('Connecting OS...')
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gokemap.settings")
print('Connecting django...')
import django
django.setup()
print('Connecting models...')
from map.models import pokemon, raid

def get_now_raid():
    resp = requests.get(f'https://leekduck.com/boss/')
    resp.raise_for_status()

    resp.encoding = 'utf-8'
    html = resp.text

    bs = bs4.BeautifulSoup(html, 'html.parser')
    name = bs.select('ul.list > li') #> div > div > p.boss-name
    tier = 0
    d = dict()
    for n in name:
        text = n.getText()
        # print(text.replace('\n', ''))
        if text.startswith('Tier'):
            tier = text[-1]
        elif text.startswith('EX'):
            tier = 5
        elif text.startswith('CP'):
            break;
        else:
            d[text.split('CP')[0].strip()] = tier
            # poke_obj = pokemon.objects.filter(name_eng=text.split('CP')[0].strip()).first()
            # if poke_obj:
            #     print(f'{poke_obj.id}, {poke_obj.name}, {text.split("CP")[0].strip()}')
            #     d[poke_obj.id] = tier
            # else:
            #     print('포켓몬을 찾을수 없음')
    return d


if __name__ == '__main__':
    print('Get data from leekduck...')
    raiding_poke = get_now_raid()
    raid_objs = raid.objects.all()
    print('Check db list...')
    for raid_obj in raid_objs:
        # 이미 등록된 레이드 포켓몬의 경우
        if raid_obj.poke.name_eng in list(raiding_poke.keys()):
            raid_obj.Tier=raiding_poke[raid_obj.poke.name_eng]
            raid_obj.ison=1
            raid_obj.save()
        # 이번 레이드 목록에 없는 경우
        else:
            raid_obj.ison=False
            raid_obj.save()
    print('Check new raid list')
    for poke_name, raid_level in raiding_poke.items():
        poke_obj = pokemon.objects.filter(name_eng=poke_name).first()
        # pokemon db에서 해당 포켓몬 아이디를 찾을 수 있는 경우
        if poke_obj:
            # 해당 포켓몬이 raid 등록이 안된 경우
            if not raid.objects.filter(poke=poke_obj.id):
                raid.objects.create(Tier=raid_level, poke=poke_obj, ison=1)
        # pokemon db에서 해당 포켓몬 아이디를 찾을 수 없없 경우
        else:
            print(f'{poke_name} dont have poke object in DB')

    for i in raid.objects.all():
        if i.ison == 1:
            print(i.poke)