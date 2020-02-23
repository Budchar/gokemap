import json, random
from django.db.models import Sum
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import knowledgePlus
from .skills import req_rsp, skillResponse, singleResponse, simple_text, SkillResponseView


@csrf_exempt
def knowledge2plus(request):
    valueList = list()
    knowObjects = knowledgePlus.objects.filter(answer__isnull=False)
    for i, know in enumerate(knowObjects):
        valueList.append([i+1, "크루 지식+", "", "", "", "", know.utterance, know.answer, "", ""])
    response = {
        "values": valueList,
        "name": "뉴크루지식더하기",
        "schema_type": "1.0"
    }
    return JsonResponse(response)
