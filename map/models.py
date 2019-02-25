from djgeojson.fields import PointField
from django.db import models
from datetime import timedelta, datetime
from django.utils import timezone

type_choice = {'normal': 'nm', 'fire': 'fr', 'water': 'wt', 'grass': 'grs', 'electric': 'et',
               'ice': 'ice', 'fighting': 'ft', 'poison': 'ps', 'ground': 'gr', 'flying': 'fl', 'psychic': 'psy',
               'bug': 'bug', 'rock': 'r', 'ghost': 'gst', 'dragon': 'dra', 'dark': 'dk', 'steel': 'stl', 'fairy': 'fry'}


# Create your models here.
class pokemon(models.Model):
    name = models.CharField(max_length=20, default="미정")
    type_1 = models.CharField(max_length=4, default="미정")
    type_2 = models.CharField(max_length=4, default="미정")
    atk = models.IntegerField(default=-1)
    df = models.IntegerField(default=-1)
    stm = models.IntegerField(default=-1)
    c_rate = models.IntegerField(default=-1)
    r_rate = models.IntegerField(default=-1)

    def __str__(self):
        return self.name

    def cp_cal(self, a, d, s, l):
        att = self.atk + a
        deff = (self.df + d) ** 0.5
        st = (self.stm + s) ** 0.5
        cmp = 0.7903 ** 2
        cp = (att * deff * st) * cmp / 10
        return cp


class research(models.Model):
    to_do = models.CharField(max_length=50, default="미정")
    rwd = models.CharField(max_length=20, default="미정")


class raid(models.Model):
    Tier = models.IntegerField(choices=[(1,1),(2,2),(3,3),(4,4),(5,5)], default=0)
    poke = models.ForeignKey(pokemon, on_delete=models.DO_NOTHING, db_constraint=False, default=-1, related_name='raid')

    def __str__(self):
        return self.poke.name


class gym(models.Model):
    name = models.CharField(max_length=50, default="미정")
    is_pkstp = models.BooleanField(default=True)  # 포켓스탑이면 1(true) 체육관이면 0(false)
    x_cdn = models.CharField(max_length=20, default=-1)
    y_cdn = models.CharField(max_length=20, default=-1)
    geom = PointField(null=True, blank=True)

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

class raid_ing(models.Model):
    gym = models.OneToOneField(gym, on_delete=models.DO_NOTHING)
    poke = models.ForeignKey(raid, on_delete=models.DO_NOTHING, blank=True, null=True)
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
    p_time = models.DateTimeField(null=True)

class event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

