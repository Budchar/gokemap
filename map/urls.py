from django.urls import path
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt
from . import views, skills_raid, skills_user, skills_research, skills_party, skills_event, skills_pokemon, skills_chat

app_name = 'map'
urlpatterns = [
    # ex: /map/
    path('', views.IndexView.as_view(), name='index'),
    url(r'^raid_report_fire/', csrf_exempt(skills_raid.reportFire.as_view())),
    url(r'^raid_report_gym/', csrf_exempt(skills_raid.reportGym.as_view())),
    url(r'^raid_report_poke/', csrf_exempt(skills_raid.reportPoke.as_view())),
    url(r'^raid_board/', csrf_exempt(skills_raid.raid_board.as_view())),
    url(r'^raid_mod/', csrf_exempt(skills_raid.mod.as_view())),
    url(r'^raid_mod_quarter/', csrf_exempt(skills_raid.mod_quarter.as_view())),
    # 재민 담당
    url(r'^chat_hello/', csrf_exempt(skills_chat.say_hello)),
    url(r'^chat_simple_answer/', csrf_exempt(skills_chat.simple_ans)),
    url(r'^chat_idiot/', csrf_exempt(skills_chat.idiot)),
    #url(r'^chat_meal/', csrf_exempt(skills_chat.meal)),
    url(r'^chat_interjection/', csrf_exempt(skills_chat.interjection)),
    url(r'^chat_distance/', csrf_exempt(skills_chat.distance)),
    # 유저 관리
    url(r'^user_enroll/', skills_user.user_enroll),
    url(r'^team_enroll/', skills_user.team_enroll),
    # 리서치 신청
    url(r'^research_post/', skills_research.post),
    url(r'^research_board/', csrf_exempt(skills_research.board.as_view())),
    # 파티 신청
    url(r'^party_post/', csrf_exempt(skills_party.post.as_view())),
    url(r'^party_board/', skills_party.board),
    url(r'^party_register/', skills_party.register),
    url(r'^party_leave/', skills_party.leave),
    url(r'^party_arrived/', skills_party.arrived),
    url(r'^party_mod_time/', skills_party.mod_time),
    url(r'^party_mod_gym/', skills_party.mod_gym),
    # 이벤트
    url(r'^event_board/', skills_event.board),
    url(r'^event_detail/', skills_event.detail),
    # 포켓몬
    url(r'^pokemon_info', skills_pokemon.info),
    url(r'^pokemon_detail', skills_pokemon.detail),
    # path('posted/', views.raid_post, name='posted'),
    # path('party/', views.party_post, name='p_posted'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)