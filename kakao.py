import requests
import json


def sendToMeMessage(text):
    header = {'Authorization': 'Bearer' + KAKAO_TOKEN}
    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
    post = {
        "object_type": "text",
        "text": text,
        "link": {
            "web_url": "",
            "mobile_web_url": ""
        },
        "button_title": "바로확인"
    }

    data = {"template_object": json.dumps(post)}
    return requests.post(url, headers=header, data=data)


text = "안녕하세요."
KAKAO_TOKEN = "CcWBhl0Ox3-06g_0O-AGHuGA275A9Z69BHRIEwo9c00AAAF8ROKnng"

result = sendToMeMessage(text)
print(result.text)