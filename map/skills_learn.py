import json, random
from django.db.models import Sum
from .models import knowledgePlus
from .skills import req_rsp, skillResponse, singleResponse, simple_text, SkillResponseView


class fallback(SkillResponseView):
    def make_response(self, request):
        description = "아직 배우지 못한 내용이에요🐥\n\n\n건의사항이 있다면 하단 폼을 통해 남겨주시거나 직접 적절한 대답을 알려주세요!"
        url = "https://forms.gle/DmArxLk5tL4D14Dv5"
        user = request.user_id
        utterance = request.received_json_data['userRequest']['utterance']
        extra = {"user":user,"utterance":utterance}
        knowledgePlus.object.create(user_id=user,utterance=utterance)
        restaurantCard = singleResponse(description=description).web_button("의견남기기", url).block_button("5e521c158192ac0001584b32", extra, "뉴크루봇에게 알려주기", "뉴크루봇에게 알려주기").card()
        response = skillResponse(Homebutton=False).input(restaurantCard).quickReply("🏠홈", "🏠홈", "5e438314ffa7480001f94123")
        return response.default


class knowledgeplus(SkillResponseView):
    def make_response(self, request):
        extra = request.client_data()
        user = extra['user']
        utterance = extra['utterance']
        answer = request.params['answer']['origin']
        knowObject, created = knowledgePlus.objects.update_or_create(user_id=user,utterance=utterance,answer=answer)
        return skillResponse(Homebutton=False).input(singleResponse(description="알려주셔서 감사합니다!").card()).quickReply("🏠홈", "🏠홈", "5e438314ffa7480001f94123")
