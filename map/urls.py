from django.urls import path
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from . import views, skills_raid, skills_user, skills_research, skills_party, skills_event

app_name = 'map'
urlpatterns = [
    # ex: /map/
    path('', views.IndexView.as_view(), name='index'),
    url(r'^raid_post/', skills_raid.post),
    url(r'^raid_board/', skills_raid.board),
    url(r'^raid_mod/', skills_raid.mod),
    url(r'^user_enroll/', skills_user.user_enroll),
    url(r'^team_enroll/', skills_user.team_enroll),
    url(r'^research_post/', skills_research.post),
    url(r'^research_board/', skills_research.board),
    url(r'^party_post/', skills_party.post),
    url(r'^party_board/', skills_party.board),
    url(r'^party_register/', skills_party.register),
    url(r'^party_leave/', skills_party.leave),
    url(r'^party_arrived/', skills_party.arrived),
    url(r'^party_mod_time/', skills_party.mod_time),
    url(r'^party_mod_gym/', skills_party.mod_gym),
    url(r'^event_board', skills_event.board),
    url(r'^event_detail', skills_event.detail),
    # path('posted/', views.raid_post, name='posted'),
    # path('party/', views.party_post, name='p_posted'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)