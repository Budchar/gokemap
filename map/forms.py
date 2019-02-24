from django.forms import ModelForm
from django.utils import timezone
from .models import raid_ing, party
from django import forms

TIME_INPUT_FORMATS = [
    '%H:%M:%S',     # '14:30:59'
    '%H:%M:%S.%f',  # '14:30:59.000200'
    '%H:%M',        # '14:30'
]
class raid_post_form(ModelForm):
    class Meta:
        model = raid_ing
        exclude = []
        widgets = {
            's_time': forms.DateTimeInput(attrs={'placeholder':'ex)18:00'}) #2006-10-25 14:30:59
        }
        labels = {
            "gym": "체육관",
            "poke": "포켓몬",
            "s_time": "출현시간",
        }


class party_post_form(ModelForm):
    def __init__(self, *args, **kwargs):
        super(party_post_form,self).__init__(*args,**kwargs) # populates the post
        self.fields['raid'].queryset = raid_ing.objects.filter(s_time__gte=(timezone.now() + timezone.timedelta(minutes=-46)))

    class Meta:
        model = party
        exclude = []
        widgets = {
            'p_time': forms.DateTimeInput(attrs={'placeholder': 'ex)18:00'})  # 2006-10-25 14:30:59
        }
        labels = {
            'raid': "레이드",
            "p_time": "시간",
        }


