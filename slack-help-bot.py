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
  def __init__(self):
    # Token Conf read 
    token = TokenInput()
    ######################
    status = 0
    heroku_time = 21600
    sc = SlackClient(token.info())
    # Check read API Token
    api_test = sc.api_call("api.test")
    if api_test["ok"] == status:
      error_message(api_test["error"])
    ######################
    # ouput of own bot info
    rtm_start = sc.api_call("rtm.start")
    if rtm_start["ok"] == status:
      error_message(rtm_start["error"])
    #######################
    bot_info = rtm_start['self']
    bot_id = bot_info["id"]
    if sc.rtm_connect():
      while True:
        data = sc.rtm_read()
        if len(data) > 0:
          for params in data:
             if "type" in params.keys():
               if params["type"] == "message":
                 if re.search(bot_id, params["text"]):
                   if re.search(u"(.*sleep.*)", params["text"]) is not None:
                     self.sleep_message(sc, params, heroku_time)
                   elif re.search(u"(.*mention.*|.*返信.*)", params["text"]) is not None:
                     self.mention_help_message(params, sc)
                   else:
                     self.default_message(params, sc)
    else:
      print("Connection Failed, invalid token?")

  # Default Message of Bot.
  def default_message(self, params, sc):
    sc.rtm_send_message("test-help-bot", "<@" + params["user"] + "> " + u"ごめんw それ分からないw")
  #####################

  # Mention Help Message of Bot.
  def mention_help_message(self, params, sc):
    if re.search(u"(.*mention.*|.*返信.*)", params["text"]) is not None:
      sc.rtm_send_message("test-help-bot", "<@" + params["user"] + "> " + u"@とSlackのIDを付けることでメンション(リプライ)メッセージが作れるよ!")

  # Sleep Message of Bot.
  def sleep_message(self, sc, params, heroku_time):
    sc.rtm_send_message("test-help-bot", "<@" + params["user"] + "> " + u"今日はもう休むよ!おやすみ!")
    time.sleep(heroku_time)
    sc.rtm_send_message("test-help-bot", u"おはよ!今日も1日頑張るよ!")
  #######################

  # connection error of Slack.
  def error_message(self, error):
    print(error)
    sys.exit()
  ############################
sbm = SlackHelpBot()