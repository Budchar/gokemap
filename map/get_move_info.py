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
from map.models import move, fastMove, chargeMove, pokemon, poke_move

class move_vals:
    def __init__(self, move_table):
        self.move_tbl = move_table
        if move_table[0].getText().strip() == 'Fast Move':
            # fast 무브의 경우, 스위치 = 0
            self.switch = 0
        else:
            # 차지무부의 경우, 스위치 = 1
            self.switch = 1

    def getMove(self):
        d = dict()
        prefix_list = ['', 'PVE_', 'PVP_']
        prefix = 0
        for move_val in self.move_tbl:
            k = move_val.select('th')[0].getText().strip().replace(' ','_').replace('*', '')
            if k == 'Base_Power': prefix += 1
            v = move_val.select('td')[0].getText().strip()
            # charge move에서 몇 charge인지 확인
            if self.switch == 1 and k == 'Charge_Energy':
                    spn = move_val.select('span')
                    v = len(spn)
            # 위 과정에서 bs4타입으로 get함수를 부르기 때문에 오류 처리 후 str로 바꾼다
            # second를 빼주는 과정
            try:
                if 'seconds' in v:
                    v = v.split()[0]
            except TypeError:
                pass
            d[f'{prefix_list[prefix]}{k}'] = v
        return d


def get_move_poke(poke_move_list):
    isLegacy = 0
    for p in poke_move_list:
        if p.get('class')[0] == 'view-header':
            if 'Legacy' in p.getText():
                # 레거시 확인
                isLegacy = 1
            continue
        # class가 "view-content"이면
        else:
            name = p.select('td.views-field-field-pokemon-image')
            poke_list = [deal_forme(n.getText().strip()) for n in name]
            for poke in poke_list:
                poke_obj = pokemon.objects.filter(name_eng=poke).first()
                if poke_obj:
                    poke_move.objects.update_or_create(pokemon=poke_obj, move=move_obj,
                                                       defaults={'isLegacy': True if isLegacy else False})
                else:
                    print(f"{poke}가 없습니다.")
    return


# 폼 여러개 때문이 이름 조정
def deal_forme(string):
    return string.replace(' Forme','').replace(' Cloak','').replace('Burmy','Burmy (Plant)')


if __name__ == '__main__':
    move_objs = move.objects.all()
    move_default_fields = [f.name for f in move._meta.fields]
    move_fast_fields = [f.name for f in fastMove._meta.fields]
    move_charge_fields = [f.name for f in chargeMove._meta.fields]
    for move_obj in move_objs:
        skill_name = move_obj.name_eng.strip().replace(' ', '-')
        print(f'Get {skill_name} data from gamepress...')
        resp = requests.get(f"https://pokemongo.gamepress.gg/pokemon-move/{skill_name}")
        if resp.status_code == 200:
            resp.raise_for_status()
            resp.encoding = 'utf-8'
            html = resp.text
            bs = bs4.BeautifulSoup(html, 'html.parser')
            move_table = bs.select('table.move-table>tr')
            move_info = move_vals(move_table).getMove()
            default_value_dict = {f:move_info[f] for f in move_default_fields if f in move_info and move_info[f]}
            move.objects.filter(id=move_obj.id).update(**default_value_dict)
            if move_info['Move_Category'] == 'Fast Move':
                detail_value_dict = {f:move_info[f] for f in move_fast_fields if f in move_info and move_info[f]}
                fastMove.objects.update_or_create(default_info=move_obj, defaults=detail_value_dict)
            else:
                detail_value_dict = {f:move_info[f] for f in move_charge_fields if f in move_info and move_info[f]}
                chargeMove.objects.update_or_create(default_info=move_obj, defaults=detail_value_dict)
            print(f"{move_obj.name} {move_info['Move_Category']} {move_info['Move_Type']}")
            poke_move_list = bs.select('div.view-pokemon-with-move > div')
            get_move_poke(poke_move_list)
        else:
            print(f"{skill_name}:{move_obj.name}은 없는 페이지 입니다")