from django.http import JsonResponse
from .skills import simple_text, SkillResponseView
from random import choice


# skill URL: http://budcha.pythonanywhere.com/map/chat_hello/
# skills_chat.say_hello
# entity: [hi_bye] 안녕 안뇽 안냥 dkssud 녕안 뇽안 하이 ㅎㅇ gd hi 헬로 hello / 잘 자 낼바 빠이 수고해  (+ 모비)
def say_hello(request):
    req = req_rsp(request)
    resp = req.received_json_Data['userRequest']['utterance']
    return JsonResponse(simple_text(resp))


# skill URL: http://budcha.pythonanywhere.com/map/chat_simple_answer/
# skills_chat.simple_ans
# entity: [simple_resp] 응 알겠어 고마워 알았어 알앗어 알겟어 응응 웅 옹 ㅇㅋ 오키 ㅇㅋㄷㅋ 오야 네 넹 넵 넵! 네넵! 넹넹 눼 늬예 누에~ 알았어요 알앗어요 알앗어여 알았어여 알겠어여 알겟어여 알겠어요 알겟어요
def simple_ans(request):
    req = req_rsp(request)
    resp_list = ["^-^ ~", "（＾ｖ＾）", "(*´﹃｀*)", "ㅎㅎㅎㅎ~", "( >_･)b", "ㅎㅎ~", "ㅎㅅㅎ", ":)", ":D"]
    resp = choice(resp_list)
    return JsonResponse(simple_text(resp))


# skill URL: http://budcha.pythonanywhere.com/map/chat_idiot/
# skills_chat.idiot
# entity: [idiot] (모비+) 바보 멍청이 멍충이 똥멍청이 똥개 모지리
def idiot(request):
    req = req_rsp(request)
    idiot_ = req.params['idiot'] #params에서 idiot key(entity)의 value(사용자 발화)
    resp_list = [idiot_+" 아니에요!", idiot_+" 아닙니다!", idiot_+" 하지 마세요!", idiot_+"아니야!", "반사!", "놀리지 마요ㅜㅜㅜ", "엉엉ㅜㅜ", "밍,,,", "힝", "뀨><?"]
    resp = choice(resp_list)
    return JsonResponse(simple_text(resp))


# skill URL: http://budcha.pythonanywhere.com/map/chat_meal/
# skills_chat.meal
# entity:
def meal(request):
    resp = skillResponse()

