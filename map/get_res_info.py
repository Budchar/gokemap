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
from map.models import pokemon, research


def get_now_research():
    resp = requests.get("https://leekduck.com/research/")
    resp.raise_for_status()

    resp.encoding = 'utf-8'
    html = resp.text

    bs = bs4.BeautifulSoup(html, 'html.parser')
    list = bs.select('ul.list > li') #> div > div > p.boss-name
    tier = 0
    d = dict()
    for n in list:
        task = n.select('div.task-text')[0].getText()
        rwd = n.select('div.reward-text')[0].getText()
        rwd_list = d.get(task, []) + [pokemon.objects.filter(name_eng=rwd).first().name]
        d[task] = rwd_list
    return d


if __name__ == '__main__':
    print('Get data from leekduck...')
    raiding_poke = get_now_research()
    print('Truncating research database...')
    research.objects.all().delete()
    print('Adding now Research List...')
    id = 1
    for k, values in raiding_poke.items():
        for v in values:
            research.objects.create(id=id,todo=k,rwd=v)
            id +=1