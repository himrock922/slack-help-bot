# - *- coding: utf-8 -*
import time
import re
import signal
import os
import sys
import multiprocessing as mp
from slackclient import SlackClient
from token_restore import TokenInput

class SlackHelpBot:
  signal.signal(signal.SIGINT, signal.SIG_DFL)
  # Token Conf read 
  token = TokenInput()
  ######################
  status = 0
  sc = SlackClient(token.info())
  # Check read API Token
  api_test = sc.api_call("api.test")
  if api_test["ok"] == status:
    print(api_test["error"])
    sys.exit()
  ######################
  # ouput of own bot info
  rtm_start = sc.api_call("rtm.start")
  if rtm_start["ok"] == status:
    print(rtm_start["error"])
    sys.exit()
  #######################
  bot_info = rtm_start['self']
  print(bot_info)
  def __init__(self):
    if SlackHelpBot.sc.rtm_connect():
      while True:
        data = SlackHelpBot.sc.rtm_read()
       
        if len(data) > 0:
          for item in data:
            SlackHelpBot.sc.rtm_send_message("test-help-bot", self.create_message(item))
            time.sleep(1)
    else:
      print("Connection Failed, invalid token?")

  def create_message(self, data):
    if "type" in data.keys():
      if data["type"] == "message":
        if re.search(u"(.*帰ります.*|.*帰宅.*)", data["text"]) is not None:
          return "<@" + data["user"] + "> " + u"お疲れ様〜。気をつけて帰ってきてね！:wink:"
  def error_message(self, error):
    print(error)
    sys.exit

sbm = SlackHelpBot()