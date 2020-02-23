from djgeojson.fields import PointField
from django.db import models
from datetime import timedelta, datetime
from django.utils import timezone


# Create your models here.
class user(models.Model):
    kid = models.CharField(max_length=100)
    nick = models.CharField(max_length=15)
    val = models.IntegerField(blank=True, null=True)
    mys = models.IntegerField(blank=True, null=True)
    ins = models.IntegerField(blank=True, null=True)
    group = models.IntegerField(default=1)


class pokemon(models.Model):
    num = models.CharField(max_length=10, default='미정')
    name = models.CharField(max_length=20, default="미정")
    name_eng = models.CharField(max_length=20, default="미정")
    type_1 = models.CharField(max_length=4, default="미정")
    type_2 = models.CharField(max_length=4, default="미정")
    atk = models.IntegerField(default=-1)
    df = models.IntegerField(default=-1)
    stm = models.IntegerField(default=-1)
    c_rate = models.FloatField(default=-1)
    r_rate = models.FloatField(default=-1)
    female_rate = models.FloatField(default=-1)
    second_candy = models.CharField(max_length=15, default='미정')
    buddy_distance = models.CharField(max_length=6, default='미정')
    evolution_candy = models.CharField(max_length=15, default='미정')
    group = models.IntegerField(default=-1)
    lv20_000 = models.IntegerField(default=-1)
    lv20_555 = models.IntegerField(default=-1)
    lv25_000 = models.IntegerField(default=-1)
    lv25_555 = models.IntegerField(default=-1)
    lv40_555 = models.IntegerField(default=-1)
    img_url = models.URLField(null=True)

    type_choice = {'normal': 'nm', 'fire': 'fr', 'water': 'wt', 'grass': 'grs', 'electric': 'et',
                   'ice': 'ice', 'fighting': 'ft', 'poison': 'ps', 'ground': 'gr', 'flying': 'fl', 'psychic': 'psy',
                   'bug': 'bug', 'rock': 'r', 'ghost': 'gst', 'dragon': 'dra', 'dark': 'dk', 'steel': 'stl',
                   'fairy': 'fry'}

    def __str__(self):
        return self.name

    def cp_cal(self, a, d, s, l):
        cmp_dic = {20: 0.59740001, 25: 0.667934}
        att = self.atk + a
        deff = (self.df + d) ** 0.5
        st = (self.stm + s) ** 0.5
        cmp = cmp_dic.get(l) ** 2
        cp = (att * deff * st) * cmp / 10
        return cp


class research(models.Model):
    todo = models.CharField(max_length=1000, default="미정")
    rwd = models.CharField(max_length=20, default="미정")


class raid(models.Model):
    Tier = models.IntegerField(choices=[(1,1),(2,2),(3,3),(4,4),(5,5)], default=0)
    poke = models.ForeignKey(pokemon, on_delete=models.DO_NOTHING, db_constraint=False, default=-1, related_name='raid')
    ison = models.BooleanField(default=False)

    def __str__(self):
        return "{0} {1}".format(self.Tier, self.poke.name)


class gym(models.Model):
    name = models.CharField(max_length=50, default="미정")
    nick = models.CharField(max_length=10, default="미정")
    x_cdn = models.CharField(max_length=20, default=-1)
    y_cdn = models.CharField(max_length=20, default=-1)
    geom = PointField(null=True, blank=True)
    img_url = models.URLField(null=True)

    def __str__(self):
        return self.name

    @property
    def icon(self):
        if(timezone.now() + timedelta(minutes=-1) >= self.raid_ing.s_time + timedelta(minutes=45)):
            return [0, 0]
        else:
            if (timezone.now() + timedelta(minutes=-1) <= self.raid_ing.s_time):
                # 시작 전엔 알
                return ["r", str(self.raid_ing.tier)]
                # 시작 후엔 포켓몬
            else: return ["p", str(self.raid_ing.poke.poke.id)]

    @property
    def n(self):
        return '<p>{}</p>'.format(self.name)


class pokestop(models.Model):
    name = models.CharField(max_length=50, default="미정")
    nick = models.CharField(max_length=10, default="미정")
    x_cdn = models.CharField(max_length=20, default=-1)
    y_cdn = models.CharField(max_length=20, default=-1)
    geom = PointField(null=True, blank=True)

    def __str__(self):
        return self.name


class raid_ing(models.Model):
    gym = models.ForeignKey(gym, on_delete=models.DO_NOTHING)
    poke = models.ForeignKey(raid, on_delete=models.SET_DEFAULT, blank=True, null=True, default=1)
    tier = models.IntegerField(choices=[(1,1),(2,2),(3,3),(4,4),(5,5)], default=0)
    s_time = models.DateTimeField(null=True)

    def e_time(self):
        if self.s_time is not None:
            return self.s_time + timedelta(minutes=45)
        else: return timezone.now() + timedelta(days=-10)

    def __str__(self):
        if (self.e_time() >= timezone.now() + timedelta(minutes=-1)):
            return str(self.gym) + " " + str(self.poke)
        else: return "-1"


class party(models.Model):
    raid = models.ForeignKey(raid_ing, on_delete=models.CASCADE)
    time = models.DateTimeField(null=True)
    description = models.TextField(blank=True, null=True, default="화력 미달시 펑")


class partyboard(models.Model):
    party = models.ForeignKey(party, on_delete=models.CASCADE)
    user = models.ForeignKey(user, on_delete=models.DO_NOTHING)
    val = models.IntegerField(blank=True, null=True)
    mys = models.IntegerField(blank=True, null=True)
    ins = models.IntegerField(blank=True, null=True)
    tag = models.TextField(blank=True, null=True)
    arrived = models.BooleanField(default=False)


class event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    img_url = models.URLField(null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return self.title


class temp(models.Model):
    date = models.DateField()
    description = models.TextField()


class move(models.Model):
    name = models.CharField(max_length=16)
    name_eng = models.CharField(max_length=32)
    Move_Category = models.CharField(max_length=16)
    Move_Type = models.CharField(max_length=16)
    Effect = models.CharField(max_length=128)
    PVE_Base_Power = models.IntegerField(default=-1)
    PVE_Damage_Per_Second = models.FloatField(default=-1)
    PVE_Damage_Window = models.FloatField(default=-1)
    PVE_Move_Cooldown = models.FloatField(default=-1)
    PVP_Base_Power = models.FloatField(default=-1)


class fastMove(models.Model):
    default_info = models.ForeignKey(move, on_delete=models.CASCADE, null=True)
    PVE_Energy_Delta = models.IntegerField(default=-1)
    PVE_Energy_Per_Second = models.FloatField(default=-1)
    PVP_Duration = models.IntegerField(default=-1)
    PVP_Energy_Delta = models.IntegerField(default=-1)
    PVP_Move_Cooldown = models.FloatField(default=-1)


class chargeMove(models.Model):
    default_info = models.ForeignKey(move, on_delete=models.CASCADE, null=True)
    PVE_Charge_Energy = models.IntegerField(default=-1)
    PVE_Damage_per_Energy = models.FloatField(default=-1)
    PVE_DPEDPS = models.FloatField(default=-1)
    PVP_Charge_Energy = models.FloatField(default=-1)
    PVP_Damage_Per_Energy = models.FloatField(default=-1)


class poke_move(models.Model):
    pokemon = models.ForeignKey(pokemon, on_delete=models.CASCADE)
    move = models.ForeignKey(move, on_delete=models.CASCADE)
    isLegacy = models.BooleanField(default=False)


class restaurant(models.Model):
    name = models.CharField(max_length=50)
    occasion = models.CharField(max_length=20)
    place = models.CharField(max_length=20)
    parentCategory = models.CharField(max_length=20)
    childCategory = models.CharField(max_length=20)
    url = models.CharField(max_length=100)


class ratedRestaurant(models.Model):
    restaurant = models.ForeignKey(restaurant, on_delete=models.CASCADE)
    user_id = models.CharField(max_length=100)
    rating = models.IntegerField(default=0)
    time = models.DateTimeField(auto_now=True, auto_now_add=False)


class knowledgePlus(models.Model):
    user_id = models.CharField(max_length=100)
    utterance = models.CharField(max_length=3000)
    answer = models.CharField(max_length=3000, null=True)