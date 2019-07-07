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

class move_vals:
    def __init__(self, move_table):
        self.vals = []
        self.move_tbl = move_table
        if move_table[0].getText().strip() == 'Fast Move':
            # fast 무브의 경우, 스위치 = 0
            self.keys = ['category', 'type', 'pve_bp', 'pve_dps', 'pve_dw', 'pve_mc', 'pve_ed', 'pve_eps', 'pvp_bp', 'pvp_d',
                     'pvp_ed', 'pvp_mc']
            self.switch = 0
        else:
            # 차지무부의 경우, 스위치 = 1
            self.keys = ['category', 'type', 'pve_bp', 'pve_dps', 'pve_ce', 'pve_dw', 'pve_mc', 'pve_dpe', 'pve_dpedps',
                       'pvp_bp', 'pvp_ce', 'pvp_dpe']
            self.switch = 1

    def getMove(self):
        for move_val in self.move_tbl:
            # charge move에서 몇 charge인지 확인
            if self.switch == 1:
                try:
                    if move_val.get('class')[0] == 'energy-bar':
                        spn = move_val.select('span')
                        self.vals.append(len(spn))
                        continue
                except TypeError:
                    pass
            # 위 과정에서 bs4타입으로 get함수를 부르기 때문에 오류 처리 후 str로 바꾼다
            move_val = move_val.getText().strip()
            # second를 빼주는 과정
            if 'seconds' in move_val:
                self.vals.append(move_val.split()[0])
                continue
            self.vals.append(move_val)
        d = {key: val for key, val in zip(self.keys, self.vals)}
        return d

if __name__ == '__main__':
    print('Get data from gamepress...')
    resp = requests.get('https://pokemongo.gamepress.gg/pokemon-move/quick-attack')
    if resp.status_code == 200:
        resp.raise_for_status()
        resp.encoding = 'utf-8'
        html = resp.text
        bs = bs4.BeautifulSoup(html, 'html.parser')
        # move_table = bs.select('table.move-table>tr>td')
        # move_info = move_vals(move_table)
        # for k, v in move_info.getMove().items():
        #     print(k, v)
        poke_move = bs.select('div.view-pokemon-with-move > div')
        for p in poke_move:
            if p.get('class')[0] == 'view-header':
                if 'Legacy' in p.getText():
                    # 레거시 확인
                    print(p.getText())
                continue
            # class가 "view-content"이면
            else:
                name = p.select('td.views-field-field-pokemon-image')
                print([n.getText().strip() for n in name])