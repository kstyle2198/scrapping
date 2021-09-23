# 파이썬에서 슬랙으로 텍스트 메시지 보내기 입니다.
import requests
import json
from secret import *

class Slack_Msg():
  def __init__(self, msg):
    self.msg = msg
    self.sendmsg()


  def sendmsg(self):
    web_hook_url = web_hook_url
    sendmsg = self.msg
    slack_msg = {'text' : sendmsg}
    requests.post(web_hook_url, data=json.dumps(slack_msg))

if __name__ == "__main__":
      Slack_Msg("test11111")

