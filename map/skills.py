import json


class req_rsp:
    def __init__(self, request):
        # json data decode
        json_str = request.body.decode('utf-8')
        # 디코드한 json data 풀어보기
        received_json_data = json.loads(json_str)
        # json 파일에서 입력값을 전달해주는 param 접근
        self.params = received_json_data['action']['detailParams']
        self.user_id = received_json_data['userRequest']['user']['id']
        self.client_data = received_json_data['action']['clientExtra']['data']


def make_simple_text_response(text):
    skill_response_default = {
            "version":"2.0",
            "template":{},
            "context":{},
            "data":{},
        }
    data = {
        "simpleText":{}
        }
    lis = list()
    data['simpleText']['text'] = text
    lis.append(data)
    skill_response_default['template']['outputs'] = lis
    return skill_response_default


def make_basic_card(title, time, extra, imgurl):
    card_form = {
        'title': title,
        'description': time,
        'thumbnail':{
            'imageUrl': imgurl,
        },
        'buttons': [
            {
                'action': 'block',
                'label': "상세 정보",
                'messageText': '이벤트 상세 정보',
                'blockId': '5c89f9ac5f38dd4767218f9d',
                'extra': {
                    'data': extra,
                }
            },
            {
                'action': 'share',
                'label': "공유하기",
            },
        ]
    }
    return card_form


def make_carousel(card_list):
    skill_response_default = {
            "version":"2.0",
            "template":{},
            "context":{},
            "data":{},
        }
    data = {
        "carousel":{
            'type': "basicCard",
            'items': card_list,
        }
    }
    lis = list()
    lis.append(data)
    skill_response_default['template']['outputs'] = lis
    return skill_response_default
